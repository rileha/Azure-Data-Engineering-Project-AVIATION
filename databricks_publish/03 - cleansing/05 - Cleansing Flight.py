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
    "to_date(concat_ws('-', cast(Year as string), lpad(cast(Month as string), 2, '0'), lpad(cast(DayofMonth as string), 2, '0')), 'yyyy-MM-dd') as date",
    "year(date) as date_year",
    "from_unixtime(unix_timestamp(CASE WHEN DepTime = 2400 THEN 0 ELSE DepTime END, 'HHmm'), 'HH:mm') as deptime",
    #"from_unixtime(unix_timestamp(CASE WHEN DepTime = 2400 THEN 0 ELSE DepTime END, 'HHmm'), 'HH:mm') as CRSDepTime",
    #"from_unixtime(unix_timestamp(CASE WHEN DepTime = 2400 THEN 0 ELSE DepTime END, 'HHmm'), 'HH:mm') as ArrTime",
    #"from_unixtime(unix_timestamp(CASE WHEN DepTime = 2400 THEN 0 ELSE DepTime END, 'HHmm'), 'HH:mm') as CRSArrTime",         
    'try_cast(TailNum as int) as tailid', 
    'UniqueCarrier as unique_carrier',
    'try_cast(FlightNum as int) flight_number',
    #'try_cast(ActualElapsedTime as int) as actual_elapsed_time',
    #'try_cast(CRSElapsedTime as int) as CRS_elapsed_time',
    #'try_cast(AirTime as int) as air_time',
    'try_cast(ArrDelay as int) as arrival_delay',
    'try_cast(DepDelay as int) as departure_delay',
    'Origin as origin',
    #'Dest as destination',
    #'Distance as distance',
    #'TaxiIn as taxi_in',
    #'TaxiOut as taxi_out',
    'Cancelled as cancelled',
    'CancellationCode as cancellation_code',
    #'Diverted as diverted',
    #'CarrierDelay as carrier_delay',
    #'WeatherDelay as weather_delay',
    #'NASDelay as NAS_delay',
    #'SecurityDelay as security_delay',
    #'LateAircraftDelay as late_aircraft_delay',
    #"to_date(Date_Part, 'yyyy-MM-dd') as Date_Part"
      #date,
)

df_base.writeStream.trigger(once=True)\
    .format('delta')\
    .option('checkpointLocation', '/dbfs/FileStore/tables/checkpointLocation/dim_flight/')\
    .start('/mnt/cleansed_datalake/dim_flight/')

# COMMAND ----------

extract_schema('dim_flight')

# COMMAND ----------

create_delta_table('flight', 'dim_flight', 'cleansed_gcdev')

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM cleansed_gcdev.dim_flight_table
