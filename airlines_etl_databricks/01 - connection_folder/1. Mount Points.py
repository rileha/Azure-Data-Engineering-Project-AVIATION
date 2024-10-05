# Databricks notebook source
# MAGIC %md
# MAGIC Blob Storage Source Mount

# COMMAND ----------

# MAGIC %scala
# MAGIC val containerName = dbutils.secrets.get(scope="gc-secret",key="containername")
# MAGIC val storageAccountName = dbutils.secrets.get(scope="gc-secret",key="storageaccountname1")
# MAGIC val sasToken = dbutils.secrets.get(scope="gc-secret",key="mount-db-storage-sas")
# MAGIC val config = "fs.azure.sas." + containerName + "." + storageAccountName + ".blob.core.windows.net"
# MAGIC val mountPoint = "/mnt/source_blob/"

# COMMAND ----------

# MAGIC %scala
# MAGIC dbutils.fs.mount(
# MAGIC   source = dbutils.secrets.get(scope="gc-secret",key="blob-mnt-path"),
# MAGIC   mountPoint = mountPoint,
# MAGIC   extraConfigs = Map(config -> sasToken))

# COMMAND ----------

dbutils.fs.unmount("/mnt/source_blob/")

# COMMAND ----------

dbutils.fs.ls("/mnt/source_blob/")

# COMMAND ----------

# MAGIC %md
# MAGIC ADLS: Raw Sink Mount

# COMMAND ----------

configs = {"fs.azure.account.auth.type": "OAuth",
           "fs.azure.account.oauth.provider.type": "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
           "fs.azure.account.oauth2.client.id": dbutils.secrets.get(scope = "gc-secret", key = "data-app-id"),
           "fs.azure.account.oauth2.client.secret": dbutils.secrets.get(scope = "gc-secret",key = "data-app-secret"),
           "fs.azure.account.oauth2.client.endpoint": dbutils.secrets.get(scope = "gc-secret", key = "data-client-refresh-url")}

mountPoint="/mnt/raw_datalake/"
if not any(mount.mountPoint == mountPoint for mount in dbutils.fs.mounts()):
  dbutils.fs.mount(
    source = dbutils.secrets.get(scope = "gc-secret", key = "datalake-raw"),
    mount_point = mountPoint,
    extra_configs = configs)

# COMMAND ----------

dbutils.fs.ls("/mnt/raw_datalake/PLANE")

# COMMAND ----------

A

# COMMAND ----------

# MAGIC %scala
# MAGIC val containerName = dbutils.secrets.get(scope="gc-secret",key="containername-manual")
# MAGIC val storageAccountName = dbutils.secrets.get(scope="gc-secret",key="storageaccountname1")
# MAGIC val sas = dbutils.secrets.get(scope="gc-secret",key="sas-manualfiles")
# MAGIC val config = "fs.azure.sas." + containerName+ "." + storageAccountName + ".blob.core.windows.net"
# MAGIC
# MAGIC dbutils.fs.mount(
# MAGIC source = dbutils.secrets.get(scope="gc-secret",key="blob-mnt-path-manualfiles"),
# MAGIC mountPoint = "/mnt/manualfiles_blob/",
# MAGIC extraConfigs = Map(config -> sas))

# COMMAND ----------

# MAGIC %md
# MAGIC Cleansed /mnt/cleansed/ in ADLS Dev Storage Account

# COMMAND ----------

configs = {"fs.azure.account.auth.type": "OAuth",
           "fs.azure.account.oauth.provider.type": "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
           "fs.azure.account.oauth2.client.id": dbutils.secrets.get(scope = "gc-secret", key = "data-app-id"),
           "fs.azure.account.oauth2.client.secret": dbutils.secrets.get(scope = "gc-secret",key = "data-app-secret"),
           "fs.azure.account.oauth2.client.endpoint": dbutils.secrets.get(scope = "gc-secret", key = "data-client-refresh-url")}

mountPoint="/mnt/cleansed_datalake/"
if not any(mount.mountPoint == mountPoint for mount in dbutils.fs.mounts()):
  dbutils.fs.mount(
    source = dbutils.secrets.get(scope = "gc-secret", key = "datalake-cleansed"),
    mount_point = mountPoint,
    extra_configs = configs)
