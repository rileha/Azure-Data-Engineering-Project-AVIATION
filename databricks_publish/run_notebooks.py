# Databricks notebook source
dbutils.widgets.text("layer_name", "")
layer_name = dbutils.widgets.getArgument("layer_name")

# COMMAND ----------

notebook_path_json = {
    "raw": ["/Workspace/gc_dev/02 - raw_sourcing/01 - pdf to csv Plane"],
    "cleansed": [
            "/Workspace/gc_dev/03 - cleansing/01 - Cleansing Plane",
            "/Workspace/gc_dev/03 - cleansing/02 - Cleansing Airport",
            "/Workspace/gc_dev/03 - cleansing/03 - Cleansing Cancellation",
            "/Workspace/gc_dev/03 - cleansing/04 - Cleansing Unique Carriers",
            "/Workspace/gc_dev/03 - cleansing/05 - Cleansing Flight",
            "/Workspace/gc_dev/03 - cleansing/06 - Cleansing Airlines",
    ],
    "data_quality_checks": ["/Workspace/gc_dev/04 - data_quality_checks/01 - data_difference_count"],
    "mart":
        [
            "/Workspace/gc_dev/05 - mart/01 - dim_plane",
            "/Workspace/gc_dev/05 - mart/02 - dim_airport",
            "/Workspace/gc_dev/05 - mart/03 - dim_cancellation",
            "/Workspace/gc_dev/05 - mart/04 - dim_unique_carriers",
            "/Workspace/gc_dev/05 - mart/05 - dim_flight",
            "/Workspace/gc_dev/05 - mart/06 - dim_airlines",
        ],
    "data_quality_mart":
        [
            "/Workspace/gc_dev/04 - data_quality_checks/02 - insert_mart_test",
            "/Workspace/gc_dev/04 - data_quality_checks/03 - execute_mart_test"
        ]
}

# COMMAND ----------

print(notebook_path_json[layer_name])

# COMMAND ----------

for notebook_paths in notebook_path_json[layer_name]:
    dbutils.notebook.run(notebook_paths, 0)
