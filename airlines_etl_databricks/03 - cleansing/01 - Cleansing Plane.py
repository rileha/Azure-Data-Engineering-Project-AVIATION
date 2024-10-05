# Databricks notebook source
# MAGIC %run /Workspace/gc_dev/Utility

# COMMAND ----------

df = spark.readStream \
    .format('cloudFiles') \
    .option('cloudFiles.format', 'csv') \
    .option('cloudFiles.schemaLocation', '/dbfs/FileStore/tables/schema/PLANE/') \
    .option('cloudFiles.inferColumnTypes', 'true') \
    .option('cloudFiles.schemaEvolutionMode', 'rescue') \
    .option('cloudFiles.rescuedDataColumn', '_rescued_data') \
    .load('/mnt/raw_datalake/extracted_data/')
    
df.display()


# COMMAND ----------

df_base = df_cleaned.selectExpr(
    'tailnum as tailid', 
    'type', 
    'manufacturer', 
    'to_date(issue_date) as issue_date', 
    'model', 
    'status', 
    'aircraft_type', 
    'engine_type', 
    "cast(year as int) as year", 
    "to_date(Date_Part, 'yyyy-MM-dd') as Date_Part"  # Convert Date_Part to date
)
df_base.writeStream \
    .trigger(once=True) \
    .format('delta') \
    .option('checkpointLocation', '/dbfs/FileStore/tables/checkpointLocation/PLANE_NEW') \
    .start('/mnt/cleansed_datalake/plane_new/')

# COMMAND ----------

create_delta_table('plane_new', 'plane_new', 'cleansed_gcdev')

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * 
# MAGIC FROM cleansed_gcdev.plane_new
