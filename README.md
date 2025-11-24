#  Real-Time Delta Lake Ingestion Pipeline

This project simulates a real-time data ingestion pipeline using Delta Lake on Databricks. It continuously appends fake data (Name, Address, Email) to a Delta table at scheduled intervals, tracks Delta versions, and sends HTML email summaries after each run.

The pipeline includes:
- Automatic fake data generation (Faker)
- Writing to a Delta table in append mode
- Tracking Delta version history and newly ingested rows
- Sending HTML email summaries after every ingestion
- **Automated scheduling every 5 minutes using Databricks Jobs**

---

##  Key Features

###  **1. Real-Time Fake Data Generation**
Creates synthetic records:
- Name  
- Address  
- Email  
With a configurable row count.

---

###  **2. Delta Lake Storage**
- Appends new rows on every run  
- Adds ingestion timestamp  
- Ensures ACID transactions  
- Supports time travel and versioning  

---

###  **3. Delta Version Tracking**
On every trigger, the pipeline automatically extracts:
- **Latest Delta version**
- **Version timestamp**
- **Recently appended rows**
- **Full Delta history entry**

---

###  **4. Automated Email Notification**
Each run sends an HTML email containing:
- Number of rows ingested  
- Current ingestion timestamp  
- Delta version & version timestamp  
- A preview table of appended rows  

---

###  **5. 5-Minute Automated Scheduling**
This notebook is scheduled via **Databricks Jobs** to run **every 5 minutes**, providing near real-time ingestion behavior.

---

##  Pipeline Flow
- Generate Fake Data → Add Timestamp → Append to Delta →
Track Version Changes → Convert to HTML → Send Email →
Scheduled Every 5 Minutes

---

##  Technologies Used

| Component | Technology |
|----------|------------|
| Compute | Azure Databricks |
| Storage | ADLS Gen2 |
| Format | Delta Lake |
| Generator | Faker |
| Notifications | SMTP Email |
| Scheduling | Databricks Jobs |
| Language | PySpark (+ Python) |

---

## Folder Structure

```plaintext
.
├── notebooks/
│   └── real_time_pipeline/ delta-table-ingestion
├── data/
│   └── fake_data_table/ fake_data_table/
├── job_scheduling_proof/
│   ├──job_scheduling_screenshots
|   └──email_summary_screenshots
├── README.md

```


