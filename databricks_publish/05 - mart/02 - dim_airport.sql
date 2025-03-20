-- Databricks notebook source
USE mart_gcdev;

-- COMMAND ----------

DELETE FROM cleansed_gcdev.airport WHERE Date_Part = '2024-10/05';

-- COMMAND ----------

DESC cleansed_gcdev.airport;

-- COMMAND ----------

CREATE TABLE IF NOT EXISTS dim_airport
(
  code STRING,
  city STRING,
  country STRING,
  airport STRING,
  Date_Part DATE
) USING DELTA 
  LOCATION 'abfss://mart@gcdevadlsdev.dfs.core.windows.net/mart_datalake/dim_airport';

-- COMMAND ----------

INSERT OVERWRITE dim_airport
SELECT
  code STRING,
  city STRING,
  country STRING,
  airport STRING,
  Date_Part DATE
FROM cleansed_gcdev.airport;
