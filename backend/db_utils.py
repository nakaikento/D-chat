from sqlalchemy import create_engine
from sqlalchemy import text
import pandas as pd

def dataframe_to_database(df, table_name):
    """Convert a pandas dataframe to a database.
        Args:
            df (dataframe): pd.DataFrame which is to be converted to a database
            table_name (string): Name of the table within the database
        Returns:
            engine: SQLAlchemy engine object
    """
    engine = create_engine(f'sqlite:///:memory:', echo=False)
    df.to_sql(name=table_name, con=engine, index=False)
    return engine

def handle_response(response):
    """Handles the response from OpenAI.

    Args:
        response (openAi response): Response json from OpenAI

    Returns:
        string: Proposed SQL query
    """
    query = response["choices"][0]["message"]["content"]
    query = "SELECT "+ query
    return query

def execute_query(engine, query):
    """Execute a query on a database.

    Args:
        engine (SQLAlchemy engine object): database engine
        query (string): SQL query

    Returns:
        df: pandas.DataFrame containing the result of the query
    """
    # with engine.connect() as conn:
    #     result = conn.execute(text(query))
    #     return result.fetchall()
    df = pd.read_sql_query(
        sql = text(query),
        con = engine
    )
    return df
