# Databricks notebook source
def extract_schema(path):
    
    # Read the Delta table to get the schema
    df = spark.read.format("delta").load(f"abfss://cleansed@gcdevadlsdev.dfs.core.windows.net/{path}/")

    # Initialize an empty schema string
    schema = ''

    # Iterate over the DataFrame schema to create the schema string
    for column in df.schema:
        schema += f"{column.name} {column.dataType.simpleString()},"

    # Remove the trailing comma
    if schema:
        schema = schema[:-1]

    return schema


def create_delta_table(table_name, path, database):
   
    # Extract the schema from the provided path
    schema = extract_schema(f'{path}')
    
    # Drop the table if it exists
    spark.sql(f"DROP TABLE IF EXISTS {database}.{table_name}")

    # Create the Delta table
    spark.sql(f"""
    CREATE TABLE IF NOT EXISTS {database}.{table_name} (
        {schema}
    ) USING delta
    LOCATION 'abfss://cleansed@gcdevadlsdev.dfs.core.windows.net/{path}/'
    """)



# COMMAND ----------

def count_check(database, operation_type, table_name, number_diff):
        # Fetch the history of the table and create a temp view
        spark.sql(f"""DESCRIBE HISTORY {database}.{table_name}""").createOrReplaceTempView("Table_Count")

        # Get the current operation's output row count
        current_count_df = spark.sql(f"""
        SELECT operationMetrics.numOutputRows
        FROM Table_Count
        WHERE version = (SELECT max(version)
        FROM Table_Count 
        WHERE trim(lower(operation)) = lower('{operation_type}'))
        """)

        # Handle null values for the current count
        if current_count_df.count() == 0 or current_count_df.first()[0] is None:
            final_count_current = 0
        else:
            final_count_current = int(current_count_df.first().numOutputRows)

        # Get the previous operation's output row count
        previous_count_df = spark.sql(f"""
        SELECT operationMetrics.numOutputRows
        FROM Table_Count
        WHERE version = (
            SELECT max(version)
            FROM Table_Count
            WHERE version < (SELECT max(version)
            FROM Table_Count 
            WHERE trim(lower(operation)) = lower('{operation_type}'))
        )
        """)

        # Handle null values for the previous count
        if previous_count_df.count() == 0 or previous_count_df.first()[0] is None:
            final_count_previous = 0
        else:
            final_count_previous = int(previous_count_df.first().numOutputRows)

        # Check if the difference exceeds the given threshold
        count_diff = final_count_current - final_count_previous

        if count_diff > number_diff:
            raise Exception(f"In {table_name} table, row count difference of {count_diff} exceeds the permitted threshold of {number_diff}.")
        else:
            print(f"In {table_name} table, row count difference is {count_diff}, within the permitted threshold of {number_diff}.")


# COMMAND ----------

def insert_test_cases(database, insert_id, insert_test_cases, insert_test_query, insert_expected_result):
    try:
        spark.sql(f"""
                CREATE TABLE IF NOT EXISTS {database}.insert_test_cases
                (id INT, 
                test_cases STRING, 
                test_query STRING,
                expected_result INT
                )""")
        
        spark.sql(f"""
                INSERT INTO {database}.insert_test_cases 
                (id, test_cases, test_query, expected_result) values({insert_id}, 
                '{insert_test_cases}', '{insert_test_query}', {insert_expected_result})
                """)
    except Exception as err:
        print("Error Occured", str(err))

# COMMAND ----------

def execute_test_case(database):
    df = spark.sql(f"""SELECT * FROM {database}.insert_test_cases;""").collect()
    for i in df:
        original_result = spark.sql(f"""{i.test_query}""").collect()
        if len(original_result) == i.expected_result:
            print("Test case has passed.")
        else:
            raise Exception(f"{test_cases} has failed.")


