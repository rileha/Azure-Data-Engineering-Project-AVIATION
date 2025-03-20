-- Databricks notebook source
USE mart_gcdev;

-- COMMAND ----------

DELETE FROM cleansed_gcdev.unique_carriers WHERE Date_Part = '2024-10/05';

-- COMMAND ----------

DESC cleansed_gcdev.unique_carriers;

-- COMMAND ----------

CREATE TABLE IF NOT EXISTS dim_unique_carriers
(
  code STRING,
  description STRING,
  Date_Part STRING
) USING DELTA 
  LOCATION 'abfss://mart@gcdevadlsdev.dfs.core.windows.net/mart_datalake/dim_unique_carriers';

-- COMMAND ----------

INSERT OVERWRITE dim_unique_carriers
SELECT
  code STRING,
  description STRING,
  Date_Part STRING
FROM cleansed_gcdev.unique_carriers;
