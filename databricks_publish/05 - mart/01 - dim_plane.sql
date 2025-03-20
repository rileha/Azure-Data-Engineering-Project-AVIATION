-- Databricks notebook source
USE mart_gcdev;

-- COMMAND ----------

DELETE FROM cleansed_gcdev.plane_new WHERE Date_Part = '2024-10/05';

-- COMMAND ----------

SELECT  
  COUNT(tailid),
  COUNT(DISTINCT(tailid))
FROM cleansed_gcdev.plane_new;

-- COMMAND ----------

DESC cleansed_gcdev.plane_new;

-- COMMAND ----------

DROP TABLE dim_plane

-- COMMAND ----------

CREATE TABLE IF NOT EXISTS dim_plane
(
  tailid STRING,
  type STRING,
  manufacturer STRING,
  issue_date DATE,
  model STRING,
  status STRING,
  aircraft_type STRING,
  engine_type STRING,
  year INT,
  Date_Part DATE
) USING DELTA 
  LOCATION 'abfss://mart@gcdevadlsdev.dfs.core.windows.net/mart_datalake/dim_plane';

-- COMMAND ----------

INSERT OVERWRITE dim_plane
SELECT
  tailid STRING,
  type STRING,
  manufacturer STRING,
  issue_date DATE,
  model STRING,
  status STRING,
  aircraft_type STRING,
  engine_type STRING,
  year INT,
  Date_Part DATE
FROM cleansed_gcdev.plane_new;
