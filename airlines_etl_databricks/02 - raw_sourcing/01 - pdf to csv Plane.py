# Databricks notebook source
# MAGIC %md
# MAGIC Not possible to use Autloader as Spark struggles with pdf so need to create a pdf to csv job that is triggered by new pdf files being uploaded into the container. We can then set up an Autoloader on the 'extracted_data' directory to immediately load the processed pdf to csv files.

# COMMAND ----------

pip install PyPDF2

# COMMAND ----------

import os
import pandas as pd
from PyPDF2 import PdfReader
from datetime import datetime

def extract_and_convert_pdf_to_csv(pdf_path, csv_output_path, predefined_columns):
    """
    Extracts text from a PDF file, identifies data for predefined columns, and saves the data in CSV format.

    Args:
    - pdf_path: Path to the input PDF file.
    - csv_output_path: Path to the output CSV file.
    - predefined_columns: List of column names to identify and structure the data.
    """

    # Read the PDF file
    try:
        reader = PdfReader(pdf_path)
        text_data = []
        for page in reader.pages:
            text_data.append(page.extract_text())
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
        return

    # Join the text data into a single string
    full_text = "\n".join(text_data)

    # Split into lines
    lines = full_text.split('\n')

    # Initialize data storage
    data_rows = []
    column_found = {col: False for col in predefined_columns}
    column_indices = {col: None for col in predefined_columns}

    # Identify column indices and structure the data
    for line in lines:
        if all(column_found.values()):
            # If all columns have been found, process the remaining lines as data
            data = line.split()  # Split based on whitespace or a specific delimiter
            if len(data) == len(predefined_columns):  # Ensure row matches header length
                data_rows.append(data)
            else:
                # Append data with missing fields
                if len(data) > len(predefined_columns):
                    data_rows.append(data[:len(predefined_columns)])
                else:
                    data_rows.append(data + [''] * (len(predefined_columns) - len(data)))
        else:
            # Attempt to find column names in the line
            words = line.split()
            for idx, col in enumerate(predefined_columns):
                if col in words and not column_found[col]:
                    column_found[col] = True
                    column_indices[col] = idx  # Capture the index of the found column

    # Convert to a DataFrame with the predefined columns
    df = pd.DataFrame(data_rows, columns=predefined_columns)
    df['Date_Part'] = datetime.now().strftime('%Y-%m-%d')
    # Save DataFrame to CSV
    df.to_csv(csv_output_path, index=False)

    

# Define paths and columns
pdf_directory = '/dbfs/mnt/raw_datalake/PLANE/'
csv_output_path = '/dbfs/mnt/raw_datalake/extracted_data/extracted_data.csv'

# Manually defined column names
predefined_columns = [
    'tailnum',
    'type',
    'manufacturer',
    'issue_date',
    'model',
    'status',
    'aircraft_type',
    'engine_type',
    'year'
]

# Process PDF files in the directory
for filename in os.listdir(pdf_directory):
    if filename.endswith('.pdf'):
        pdf_path = os.path.join(pdf_directory, filename)
        extract_and_convert_pdf_to_csv(pdf_path, csv_output_path, predefined_columns)

df = pd.read_csv('/dbfs/mnt/raw_datalake/extracted_data/extracted_data.csv')
df.display()
