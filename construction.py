import json
import os
import argparse

from tqdm import tqdm
from openai import OpenAI
from dotenv import load_dotenv


from utils.spider import load_tables

load_dotenv()

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--questions", type=str, required=True)

    # chat completion parameters
    parser.add_argument("--model", default="gpt-4o-mini", type=str, help="The model to use for the SQL generation.")
    parser.add_argument("--temperature", default=0.0, type=float, help="The temperature for the SQL generation, between 0 and 2.0.")
    parser.add_argument("--max_tokens", default=1000, type=int, help="The maximum number of tokens to generate.")
    return parser.parse_args()


def main(args):

    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "<your OpenAI API key if not set as env var>"))

    system_prompt = """You are an expert SQL assistant specialized in converting natural language queries into accurate SQL statements. You:
    1. Understand database schemas and relationships
    2. Generate standard SQL queries that follow best practices
    3. Consider edge cases and data validation
    4. Can handle complex joins, aggregations, and nested queries
    5. Provide explanations for the generated SQL when needed
    
    When given a question, you will convert it to a valid SQL query based on the provided database schema."""

    print ("Reading questions from ", args.questions)

    # Load questions from JSON file
    with open(args.questions, 'r') as f:
        questions = json.load(f)

    print ("Total number of questions: ", len(questions))


if __name__ == "__main__":
    args = parse_args()
    main(args)

