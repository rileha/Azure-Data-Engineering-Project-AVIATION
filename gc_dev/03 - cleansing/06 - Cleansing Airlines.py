# Databricks notebook source
# MAGIC %run /Workspace/gc_dev/Utility

# COMMAND ----------

from pyspark.sql.functions import explode

df = spark.read.json('/mnt/raw_datalake/airlines/')
df1 = df.select(explode('response'), 'Date_Part')
df_final = df1.select("col.*", 'Date_Part')
df_final.display()

# COMMAND ----------

df_final.write.format('delta').mode('overwrite').save('/mnt/cleansed_datalake/airlines/')

# COMMAND ----------

create_delta_table('airlines', 'airlines', 'cleansed_gcdev')

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * 
# MAGIC FROM cleansed_gcdev.airlines
