def create_table_definition_prompt(df, table_name):
    """This function creates a prompt for the OpenAI API to generate SQL queries.

    Args:
        df (dataframe): pd.DataFrame object to automtically extract the table columns
        table_name (string): Name of the table within the database

        Returns: string containing the prompt for OpenAI
    """
    
    prompt = '''### sqlite table, with its properties:
#
# {}({})
#
'''.format(table_name, ",".join(str(x) for x in df.columns))
    
    return prompt

