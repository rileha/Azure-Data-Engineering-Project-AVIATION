# Databricks notebook source
# MAGIC %run /Workspace/gc_dev/Utility

# COMMAND ----------

df = (
    spark.readStream\
    .format('cloudFiles')\
    .option('cloudFiles.format', 'parquet')\
    .option('cloudFiles.schemaLocation', '/dbfs/FileStore/tables/schema/UNIQUE_CARRIERS')\
    .load('/mnt/raw_datalake/UNIQUE_CARRIERS/')
)

# COMMAND ----------

from pyspark.sql import functions as F

df_base = df.selectExpr(
    "replace(Code, '\"', '') as code",
    "replace(Description, '\"', '') as description",
    "to_date(Date_Part, 'yyyy-MM-dd') as Date_Part",
)

df_base.writeStream.trigger(once=True)\
    .format('delta')\
    .option('checkpointLocation', '/dbfs/FileStore/tables/checkpointLocation/UNIQUE_CARRIERS')\
    .start('/mnt/cleansed_datalake/unique_carriers/')

# COMMAND ----------

create_delta_table('unique_carriers', 'unique_carriers', 'cleansed_gcdev')

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * 
# MAGIC FROM cleansed_gcdev.unique_carriers
