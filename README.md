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

Please download and unzip the spider dataset from [here](https://drive.google.com/file/d/1403EGqzIDoHMdQF4c9Bkyl7dZLZ5Wt6J/view). Put the unzipped folder in the `datasets/spider_data` folder.


## Structure

## Generate predictions

Please use run the construction.py to generate predicted SQL queries. You can change the prompts in the construction.py file.

## Evaluate predictions

Please run the evaluation/evaluation.py to evaluate the predicted SQL queries. A json file containing the incorrect queries will be generated in the same directory as the predicted SQL queries.
