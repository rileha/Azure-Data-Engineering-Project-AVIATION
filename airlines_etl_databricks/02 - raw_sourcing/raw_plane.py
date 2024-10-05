# Databricks notebook source
# MAGIC %pip install pdfplumber

# COMMAND ----------

from datetime import date
from pyspark.sql import SparkSession

import pdfplumber
import pandas as pd

# Create Directory
spark = SparkSession.builder.getOrCreate()
today = str(date.today())
output_dir = f'/mnt/raw_datalake/PLANE/Date_Part={today}'
dbutils.fs.mkdirs(output_dir)

# COMMAND ----------

# Define the file path of the PDF
blob_container = 'source_blob'
storage_account_name = 'gcdevsourcestorage'
file_path = f"/dbfs/mnt/{blob_container}/PLANE.pdf"

# Read the PDF file using pdfplumber
with pdfplumber.open(file_path) as pdf:
    text_data = []
    for page in pdf.pages:
        text = page.extract_text()
        text_data.append(text)

# Convert the text data into a Pandas DataFrame
pdf_df = pd.DataFrame(text_data, columns=['Content'])

# Convert the Pandas DataFrame into a Spark DataFrame
spark_df = spark.createDataFrame(pdf_df)

# Show the extracted PDF content
spark_df.show(truncate=False)


# COMMAND ----------

#Write file to Directory
spark_df.write.mode('overwrite').option('header', 'true').csv(output_dir)
