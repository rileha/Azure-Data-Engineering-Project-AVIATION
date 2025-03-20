# Databricks notebook source
# MAGIC %run /Workspace/gc_dev/Utility

# COMMAND ----------

insert_query = """SELECT COUNT(*) AS code_count, code FROM mart_gcdev.dim_unique_carriers GROUP BY code HAVING Count(*) > 1;"""

insert_test_cases("mart_gcdev", 1, "Check if code is duplicated in dim_unique_carrier or not", insert_query, 0)

# COMMAND ----------

insert_query = """SELECT COUNT(*) AS code_count, code FROM mart_gcdev.dim_airport GROUP BY code HAVING Count(*) > 1;"""

insert_test_cases("mart_gcdev", 2, "Check if code is duplicated in dim_airport or not", insert_query, 0)
