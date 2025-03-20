-- Databricks notebook source
USE mart_gcdev;

-- COMMAND ----------

DELETE FROM cleansed_gcdev.cancellation WHERE Date_Part = '2024-10/05';

-- COMMAND ----------

DESC cleansed_gcdev.cancellation;

-- COMMAND ----------

CREATE TABLE IF NOT EXISTS dim_cancellation
(
  code STRING,
  description STRING,
  Date_Part DATE
) USING DELTA 
  LOCATION 'abfss://mart@gcdevadlsdev.dfs.core.windows.net/mart_datalake/dim_cancellation';

-- COMMAND ----------

INSERT OVERWRITE dim_cancellation
SELECT
  code STRING,
  description STRING,
  Date_Part DATE
FROM cleansed_gcdev.cancellation;
