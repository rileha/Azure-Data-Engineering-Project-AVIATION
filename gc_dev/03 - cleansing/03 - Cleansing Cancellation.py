# Databricks notebook source
# MAGIC %run /Workspace/gc_dev/Utility

# COMMAND ----------

df = (
    spark.readStream\
    .format('cloudFiles')\
    .option('cloudFiles.format', 'parquet')\
    .option('cloudFiles.schemaLocation', '/dbfs/FileStore/tables/schema/Cancellation')\
    .load('/mnt/raw_datalake/Cancellation/')
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
    .option('checkpointLocation', '/dbfs/FileStore/tables/checkpointLocation/Cancellation')\
    .start('/mnt/cleansed_datalake/cancellation/')

# COMMAND ----------

create_delta_table('cancellation', 'cancellation', 'cleansed_gcdev')

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * 
# MAGIC FROM cleansed_gcdev.cancellation
