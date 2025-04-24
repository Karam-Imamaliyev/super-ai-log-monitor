#  Super AI Log Monitor

**Super AI Log Monitor** is a real-time anomaly detection system that monitors log files, detects suspicious patterns using AI, and provides insights via a web dashboard.  
Built for developers, analysts, and security teams who need automated monitoring of log behavior.

---

##  Features

- 📡 **Real-time log monitoring** with `watchdog`
- 🤖 **Anomaly detection** using unsupervised machine learning (`IsolationForest`)
- 📊 **Feature engineering** with entropy, message length, and IP frequency
- 🛠️ **Modular architecture** (easy to extend & maintain)
- 🌐 **Streamlit dashboard** to view anomalies and log details
- ☁️ **AWS S3 integration** to export logs

---

### Tech Stack & Tools Used

| Category            | Tools / Libraries                          |
|---------------------|--------------------------------------------|
| **Language**         | Python 3.12                                |
| **ML Model**         | `sklearn.ensemble.IsolationForest`         |
| **Feature Tools**    | Custom entropy calc, IP count cache        |
| **File Monitoring**  | `watchdog`                                 |
| **Dashboard**        | `streamlit`                                |
| **Database**         | `SQLite3` (via `pandas.read_sql_query`)    |
| **AWS Export**       | `boto3` to push `.log` files to S3         |

---

## ------------------- How to Run & Test Locally --------------------- 

### 1. Install Requirements
```bash
pip install -r requirements.txt
```

### 2. Set up Configuration
Update `config/settings.yaml`:
```yaml
log_file_path: ./data/mylog_button.log
database:
  path: ./db/anomalies.db
model:
  contamination: 0.05
  random_state: 42
```

### 3. Start Real-Time Monitoring
```bash
python src/monitor.py
```

### 4.  Launch Dashboard
```bash
streamlit run dashboard.py
```

> Logs will automatically be detected, analyzed, written to `anomalies.db`, and visualized on the dashboard.

---

##  Export Logs to S3
Click the **Upload to S3** button in the dashboard  
Or run:
```bash
python upload_to_s3.py
```

---

##  Folder Structure (Shortened) (In case of errors in running, check the tree due to complex directory, it can be happen - raw tree from terminal)
```
├── ai-log-monitor
│   ├── anomaly_export.csv
│   ├── config
│   │   └── settings.yaml
│   ├── dashboard.py
│   ├── data
│   │   ├── mylog_button.log
│   │   └── mylog.log
│   ├── db
│   │   └── anomalies.db
│   ├── logs
│   │   └── anomalies.log
│   ├── main.py
│   ├── models
│   ├── requirements.txt
│   ├── src
│   │   ├── ai_model.py
│   │   ├── anomaly_features.py
│   │   ├── cloud_logger.py
│   │   ├── config_loader.py
│   │   ├── db_writer.py
│   │   ├── feature_pipeline.py
│   │   ├── __init__.py
│   │   ├── log_reader.py
│   │   ├── monitor.py
│   │   ├── __pycache__
│   │   │   ├── ai_model.cpython-312.pyc
│   │   │   ├── anomaly_features.cpython-312.pyc
│   │   │   ├── cloud_logger.cpython-312.pyc
│   │   │   ├── config_loader.cpython-312.pyc
│   │   │   ├── db_writer.cpython-312.pyc
│   │   │   ├── feature_pipeline.cpython-312.pyc
│   │   │   ├── __init__.cpython-312.pyc
│   │   │   ├── log_reader.cpython-312.pyc
│   │   │   ├── monitor.cpython-312.pyc
│   │   │   └── utils.cpython-312.pyc
│   │   ├── test_cloud_log.py
│   │   └── utils.py
│   └── upload_to_s3.py
└── aws_test.py

```

---

##  Notes

-  Sensitive logs (raw or db) are excluded from GitHub via `.gitignore`.
-  Model is unsupervised — no need for labeled training data.
-  Project developed and maintained by Karam Imamaliyev

---

##  Credits

Built with vision, precision, and leadership by Der King for BARS KRAFT 
_„Nur Logs zeigen, was Systeme wirklich fühlen.“_
