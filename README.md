# KGText2SQL

## Setup

### Install dependencies

```bash
pip install -r requirements.txt
```

### Download punkt_tab

In your terminal or jupyter notebook, please run the following command to download the punkt_tab:

```python
import nltk
nltk.download('punkt_tab')
```

### Download databases

Please download and unzip the spider dataset from [here](https://drive.google.com/file/d/1403EGqzIDoHMdQF4c9Bkyl7dZLZ5Wt6J/view). Put the unzipped files in the `datasets/spider_data` folder.


## How to use

### OpenAI API key

Please set your OpenAI API key in the `.env` file in the root directory using the following format:

```
OPENAI_API_KEY=your_openai_api_key
```

### Generate predictions

Please use run the predict.py to generate predicted SQL queries. You can change the prompts in the predict.py file.

```bash
python predict.py \
    --input datasets/spider_data/dev.json \
    --output results/predicted.sql \
    --dir datasets/spider_data \
    --tables tables.json \
    --db database \
    --model gpt-3.5-turbo \
    --temperature 0.0 \
    --max_tokens 1000
```


### Evaluate predictions

Please run the evaluation/evaluation.py to evaluate the predicted SQL queries. A json file containing the incorrect queries will be generated in the same directory as the predicted SQL queries if the `--output` argument is not specified.

```bash
python evaluation/evaluation.py \
    --gold datasets/spider_data/dev.json \
    --pred results/predicted.sql \
    --tables datasets/spider_data/tables.json \
    --db datasets/spider_data/database \
    --etype exec \
    --output results/incorrect.json
```

