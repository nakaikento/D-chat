# Dataset based on #https://www.kaggle.com/datasets/kyanyoga/sample-sales-data

import os
import logging
import pandas as pd
import openai
from backend.db_utils import dataframe_to_database, handle_response, execute_query
from backend.openai_utils import create_table_definition_prompt, combine_prompts, send_to_openai

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

def run_llm(user_input:str):
    openai.api_key = os.environ["OPENAI_API_KEY"]
    logging.info("Loading data...")
    df = pd.read_csv("backend/data/sales_data_sample.csv")
    logging.info(f"Data Format: {df.shape}")

    logging.info("Converting to database...")
    database = dataframe_to_database(df, "Sales")
    
    fixed_sql_prompt = create_table_definition_prompt(df, "Sales")
    logging.info(f"Fixed SQL Prompt: {fixed_sql_prompt}")

    logging.info("Waiting for user input...")
    # user_input = openai_utils.user_query_input()
    final_prompt = combine_prompts(fixed_sql_prompt, user_input)
    logging.info(f"Final Prompt: {final_prompt}")

    logging.info("Sending to OpenAI...")
    response = send_to_openai(final_prompt)
    proposed_query_postprocessed = handle_response(response)
    logging.info(f"Response obtained. Proposed sql query: {proposed_query_postprocessed}")
    result = execute_query(database, proposed_query_postprocessed)
    logging.info(f"Result: {result}")
    return proposed_query_postprocessed, result