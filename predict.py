import json
import os
import argparse
import sqlite3

from tqdm import tqdm
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path

from utils.spider import load_tables

load_dotenv()

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, default="datasets/spider_data/dev.json")
    parser.add_argument("--output", type=str, default="results/dev_pred.sql")
    parser.add_argument("--dir", type=str, default="datasets/spider_data")
    parser.add_argument("--tables", type=str, default="tables.json")
    parser.add_argument("--db", type=str, default="database")

    # chat completion parameters
    parser.add_argument("--model", default="gpt-4o-mini", type=str, help="The model to use for the SQL generation.")
    parser.add_argument("--temperature", default=0.0, type=float, help="The temperature for the SQL generation, between 0 and 2.0.")
    parser.add_argument("--max_tokens", default=1000, type=int, help="The maximum number of tokens to generate.")
    return parser.parse_args()


def main(args):

    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "<your OpenAI API key if not set as env var>"))

    system_prompt = """You are an expert SQL assistant specialized in converting natural language queries into accurate SQLite queries.
    When given a question, you will convert it to a valid SQLite query based on the provided database schema.
    Output ONLY the SQL query without any additional formatting - no markdown, no code blocks, no backticks, no 'sql' prefix."""    

    # Load questions from JSON file
    print ("Reading questions from ", args.input)
    with open(args.input, 'r') as f:
        examples = json.load(f)
    print ("Total number of questions: ", len(examples))

    # load schemas for all the DBs
    print ("Loading schemas...")
    schemas, _ = load_tables([os.path.join(args.dir, args.tables)])

    # Backup in-memory copies of all the DBs and create the live connections
    print ("Loading DB connections...")
    for db_id, schema in tqdm(schemas.items(), desc="DB connections"):
        sqlite_path = Path(args.dir) / args.db / db_id / f"{db_id}.sqlite"
        source: sqlite3.Connection
        with sqlite3.connect(str(sqlite_path)) as source:
            dest = sqlite3.connect(':memory:')
            dest.row_factory = sqlite3.Row
            source.backup(dest)
        schema.connection = dest

    # Get all the CREATE statements for all the DBs
    db_schemas = {}
    for db_id, _ in schemas.items():
        connection = schemas[db_id].connection
        cursor = connection.cursor()
        # Query sqlite_master table to get all CREATE statements
        cursor.execute("""
            SELECT sql 
            FROM sqlite_master 
            WHERE type='table' AND sql IS NOT NULL
        """)
        # Convert list of tuples to a single string of CREATE statements
        create_statements = '\n'.join(row[0] for row in cursor.fetchall())
        db_schemas[db_id] = create_statements

    predicted_sqls = []

    # Generate SQL queries for each question using OpenAI API
    for example in tqdm(examples, desc="Generating SQL queries"):
        question = example["question"]
        db_id = example["db_id"]
        code_representation = db_schemas[db_id]

        user_prompt = f"""### Database Schema:
        {code_representation}
        ### Question:
        {question}
        ### SQL Query:
        """

        response = client.chat.completions.create(
            model=args.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=args.temperature,
            max_tokens=args.max_tokens,
        )

        predicted_sql = response.choices[0].message.content.strip().replace('\n', ' ').replace('    ', ' ')
        predicted_sqls.append(predicted_sql)

    # make sure the output directory exists
    os.makedirs(os.path.dirname(args.output), exist_ok=True)

    # write the predicted SQLs to sql file where each line is a SQL query
    print ("Writing predicted SQLs to ", args.output)
    with open(args.output, 'w') as f:
        for sql in predicted_sqls:
            f.write(sql + '\n')

if __name__ == "__main__":
    args = parse_args()
    main(args)

