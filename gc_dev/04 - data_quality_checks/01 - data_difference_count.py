# Databricks notebook source
# MAGIC %run /Workspace/gc_dev/Utility

# COMMAND ----------

list_table_info = [
    ('Streaming Update', 'plane_new', 5000), 
    ('Streaming Update', 'flight', 100), 
    ('Streaming Update', 'airport', 100), 
    ('Streaming Update', 'cancellation', 100), 
    ('Streaming Update', 'unique_carriers', 100), 
    ('Write', 'airlines', 100)
    ]

for i in list_table_info:
    count_check('cleansed_gcdev', i[0], i[1], i[2])

