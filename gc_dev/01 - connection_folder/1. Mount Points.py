# Databricks notebook source
# MAGIC %md
# MAGIC Blob Source source

# COMMAND ----------

# MAGIC %scala
# MAGIC val containerName = dbutils.secrets.get(scope="gc-secret",key="containername")
# MAGIC val storageAccountName = dbutils.secrets.get(scope="gc-secret",key="storageaccountname1")
# MAGIC val sasToken = dbutils.secrets.get(scope="gc-secret",key="mount-db-storage-sas")
# MAGIC val config = "fs.azure.sas." + containerName + "." + storageAccountName + ".blob.core.windows.net"
# MAGIC val mountPoint = "/mnt/source_blob/"
# MAGIC
# MAGIC dbutils.fs.mount(
# MAGIC   source = dbutils.secrets.get(scope="gc-secret",key="blob-mnt-path"),
# MAGIC   mountPoint = mountPoint,
# MAGIC   extraConfigs = Map(config -> sasToken))

# COMMAND ----------

# MAGIC %md
# MAGIC ADLS Sink raw

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

# MAGIC %md
# MAGIC Blob Source manualfiles

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
# MAGIC ADLS Sink cleansed

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

# COMMAND ----------

# MAGIC %md
# MAGIC ADLS Sink mart

# COMMAND ----------

configs = {"fs.azure.account.auth.type": "OAuth",
           "fs.azure.account.oauth.provider.type": "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
           "fs.azure.account.oauth2.client.id": dbutils.secrets.get(scope = "gc-secret", key = "data-app-id"),
           "fs.azure.account.oauth2.client.secret": dbutils.secrets.get(scope = "gc-secret",key = "data-app-secret"),
           "fs.azure.account.oauth2.client.endpoint": dbutils.secrets.get(scope = "gc-secret", key = "data-client-refresh-url")}

mountPoint="/mnt/mart_datalake/"
if not any(mount.mountPoint == mountPoint for mount in dbutils.fs.mounts()):
  dbutils.fs.mount(
    source = dbutils.secrets.get(scope = "gc-secret", key = "datalake-mart"),
    mount_point = mountPoint,
    extra_configs = configs)
