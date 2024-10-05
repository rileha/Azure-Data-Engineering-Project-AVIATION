# Databricks notebook source
# MAGIC %run /Workspace/gc_dev/Utility

# COMMAND ----------

df = (
    spark.readStream\
    .format('cloudFiles')\
    .option('cloudFiles.format', 'csv')\
    .option('cloudFiles.schemaLocation', '/dbfs/FileStore/tables/schema/flight')\
    .load('/mnt/raw_datalake/flight/')
)

# COMMAND ----------

from pyspark.sql import functions as F

df_base = df.selectExpr(
    'TailNum as tailid', 
    'Year as year', 
    'Month as month', 
    'DayofMonth as day_of_month', 
    'DayOfWeek as day_of_week', 
    'DepTime as departure_time', 
    'CRSDepTime as CRS_departure_time', 
    'ArrTime as arrival_time', 
    'CRSArrTime as CRS_arrival_time', 
    'UniqueCarrier as unique_carrier',
    'FlightNum as flight_number',
    'ActualElapsedTime as actual_elapsed_time',
    'CRSElapsedTime as CRS_elapsed_time',
    'AirTime as air_time',
    'ArrDelay as arrival_delay',
    'DepDelay as departure_delay',
    'Origin as origin',
    'Dest as destination',
    'Distance as distance',
    'TaxiIn as taxi_in',
    'TaxiOut as taxi_out',
    'Cancelled as cancelled',
    'CancellationCode as cancellation_code',
    'Diverted as diverted',
    'CarrierDelay as carrier_delay',
    'WeatherDelay as weather_delay',
    'NASDelay as NAS_delay',
    'SecurityDelay as security_delay',
    'LateAircraftDelay as late_aircraft_delay',
    "to_date(Date_Part, 'yyyy-MM-dd') as Date_Part"
)

df_base.writeStream.trigger(once=True)\
    .format('delta')\
    .option('checkpointLocation', '/dbfs/FileStore/tables/checkpointLocation/flight')\
    .start('/mnt/cleansed_datalake/flight/')

# COMMAND ----------

pre_schema('/mnt/cleansed_datalake/flight/')

# COMMAND ----------

create_delta_table('flight', 'flight', 'cleansed_gcdev')

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM cleansed_gcdev.flight
