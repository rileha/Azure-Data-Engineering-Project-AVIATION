-- Databricks notebook source
USE mart_gcdev;

-- COMMAND ----------

DELETE FROM cleansed_gcdev.airlines WHERE Date_Part = '2024-10/05';

-- COMMAND ----------

DESC cleansed_gcdev.airlines;

-- COMMAND ----------

CREATE TABLE IF NOT EXISTS dim_airlines
(
  iata_code STRING,
  icao_code STRING,
  name STRING,
  Date_Part DATE
) USING DELTA 
  LOCATION 'abfss://mart@gcdevadlsdev.dfs.core.windows.net/mart_datalake/dim_airlines';

-- COMMAND ----------

INSERT OVERWRITE dim_airlines
SELECT
  iata_code STRING,
  icao_code STRING,
  name STRING,
  Date_Part DATE
FROM cleansed_gcdev.airlines;

-- COMMAND ----------

SELECT *
FROM dim_airlines;
