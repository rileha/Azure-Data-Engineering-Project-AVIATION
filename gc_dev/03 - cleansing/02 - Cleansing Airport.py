# Databricks notebook source
# MAGIC %run /Workspace/gc_dev/Utility

# COMMAND ----------

df = (
    spark.readStream\
    .format('cloudFiles')\
    .option('cloudFiles.format', 'csv')\
    .option('cloudFiles.schemaLocation', '/dbfs/FileStore/tables/schema/Airport')\
    .load('/mnt/raw_datalake/Airport/')
)

# COMMAND ----------

from pyspark.sql import functions as F

df_base = df.selectExpr(
    'Code as code',
    "split(Description, ',')[0] as city",
    "split(split(Description, ',')[1], ':')[0] as country",
    "split(split(Description, ',')[1], ':')[1] as airport",
)
df_base = df_base.withColumn('Date_Part', F.current_date())

df_base.writeStream.trigger(once=True)\
    .format('delta')\
    .option('checkpointLocation', '/dbfs/FileStore/tables/checkpointLocation/Airport')\
    .start('/mnt/cleansed_datalake/airport/')

# COMMAND ----------

create_delta_table('airport', 'airport', 'cleansed_gcdev')

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * 
# MAGIC FROM cleansed_gcdev.airport
