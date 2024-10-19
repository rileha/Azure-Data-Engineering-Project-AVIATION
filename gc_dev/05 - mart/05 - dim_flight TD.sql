-- Databricks notebook source
USE mart_gcdev;

-- COMMAND ----------

DELETE FROM cleansed_gcdev.flight WHERE Date_Part = '2024-10/05';

-- COMMAND ----------

DESC cleansed_gcdev.flight;

-- COMMAND ----------

SELECT 
  date,
  tailid,
  deptime,
  arrival_delay,
  departure_delay,
  origin,
  cancelled,
  cancellation_code,
  unique_carrier,
  flight_number 
FROM cleansed_gcdev.flight
WHERE flight_number = 2891;

-- COMMAND ----------

DROP TABLE IF EXISTS flight_report;


-- COMMAND ----------

-- MAGIC %py
-- MAGIC dbutils.fs.rm('/mnt/mart_datalake/flight_report', True)

-- COMMAND ----------

CREATE TABLE IF NOT EXISTS flight_report
(
  date date,
  year(date) as date_year,
  arrival_delay int,
  departure_delay int,
  origin string,
  cancelled string,
  cancellation_code string,
  unique_carrier string,
  flight_number int,
  tailid string,
  deptime string
) 
USING DELTA
LOCATION 'abfss://mart@gcdevadlsdev.dfs.core.windows.net/mart_datalake/flight_report'

-- COMMAND ----------

-- MAGIC %py
-- MAGIC max_year = spark.sql("""
-- MAGIC           SELECT year(max(date))
-- MAGIC           FROM cleansed_gcdev.flight""").collect()[0][0]
-- MAGIC print(max_year)

-- COMMAND ----------

INSERT OVERWRITE flight_report
SELECT
  date,
  year(date) as date_year,
  arrival_delay,
  departure_delay,
  origin,
  cancelled,
  cancellation_code,
  unique_carrier,
  flight_number,
  tailid,
  deptime
FROM cleansed_gcdev.flight;
