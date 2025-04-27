# export_csv.py

import os
import sqlite3
import pandas as pd

# Yollar
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "db", "anomalies.db")
EXPORT_PATH = os.path.join(BASE_DIR, "anomaly_export.csv")

def export_anomalies_to_csv():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM anomalies", conn)
    df.to_csv(EXPORT_PATH, index=False)
    conn.close()
    print(f"[EXPORT] Anomalies exported to: {EXPORT_PATH}")

if __name__ == "__main__":
    export_anomalies_to_csv()
