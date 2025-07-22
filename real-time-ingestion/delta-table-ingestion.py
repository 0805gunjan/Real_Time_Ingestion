# Databricks notebook source
!pip install faker pytz

# COMMAND ----------

# MAGIC %pip install yagmail

# COMMAND ----------

# MAGIC %md
# MAGIC ## Generate Fake Data and Append to delta table

# COMMAND ----------

from pyspark.sql.functions import current_timestamp
from datetime import datetime
import pandas as pd
from faker import Faker

# Initialize
fake = Faker()
row_count = 10  # or any dynamic value
data = [(fake.name(), fake.address(), fake.email()) for _ in range(row_count)]
columns = ["Name", "Address", "Email"]

# Create DataFrame and add timestamp
df = spark.createDataFrame(data, columns)

# Set Spark session time zone
spark.conf.set("spark.sql.session.timeZone", "Asia/Kolkata")

df = df.withColumn("ingestion_timestamp", current_timestamp())

# Save path
delta_path = "abfss://delta-ingestion@realtimedeltastorage.dfs.core.windows.net/fake_data_table1"

# Append to Delta Table
df.write.format("delta").mode("append").save(delta_path)


# COMMAND ----------

# MAGIC %md
# MAGIC ### Track Delta Version and New Changes

# COMMAND ----------

from delta.tables import DeltaTable

# Load table
delta_table = DeltaTable.forPath(spark, delta_path)

# Get latest version (max ingestion_timestamp)
latest_data = delta_table.toDF().orderBy("ingestion_timestamp", ascending=False).limit(row_count)

# Collect for email
latest_data_pd = latest_data.toPandas()
html_table = latest_data_pd.to_html(index=False)

delta_table.history().show() 


# COMMAND ----------

history = delta_table.history(1).select("version", "timestamp").collect()
latest_version = history[0]["version"]
version_timestamp = history[0]["timestamp"]

# COMMAND ----------

# MAGIC %md
# MAGIC ### Send HTML Email with Summary

# COMMAND ----------

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Email Setup
sender = "gunjanagrawal0805@gmail.com"
receiver = "gunjanagra08@gmail.com"
subject = "📈 Delta Table Update - Fake Data Ingestion"

# Create HTML message
html = f"""
<html>
<head></head>
<body>
  <h2>✅ Fake Data Ingestion Complete</h2>
  <p><strong>Rows Appended:</strong> {row_count}</p>
  <p><strong>Ingestion Timestamp:</strong> {datetime.now()}</p>
  <p><strong>Delta Table Version:</strong> {latest_version}</p>
  <p><strong>Version Timestamp:</strong> {version_timestamp}</p>
  <h3>📄 Appended Data Preview</h3>
  {html_table}
</body>
</html>
"""

msg = MIMEMultipart("alternative")
msg["Subject"] = subject
msg["From"] = sender
msg["To"] = receiver
msg.attach(MIMEText(html, "html"))

# Send
with smtplib.SMTP("smtp.gmail.com", 587) as server:
    server.starttls()
    server.login("gunjanagrawal0805@gmail.com", "glwj xvui sccj umen")
    server.sendmail(sender, receiver, msg.as_string())
