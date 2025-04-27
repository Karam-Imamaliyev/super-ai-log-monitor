import sqlite3
import os
import pandas as pd

class AnomalyDatabase:
    def __init__(self, db_path=None):
        if db_path is None:
            db_path = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "..", "..", "db", "anomalies.db")
            )
            print(f"[DEBUG] Database path: {db_path}")

        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._create_table()

    def _create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS anomalies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            level TEXT,
            message TEXT,
            score REAL
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def insert_anomaly(self, timestamp: str, level: str, message: str, score: float):
        query = """
        INSERT INTO anomalies (timestamp, level, message, score)
        VALUES (?, ?, ?, ?)
        """
        try:
            self.conn.execute(query, (timestamp, level, message, score))
            self.conn.commit()
            print("[DEBUG] Anomaly successfully written to DB")
        except sqlite3.Error as e:
            print(f"[ERROR] SQL Error: {e}")

    def close(self):
        self.conn.close()


def export_anomalies_to_csv(output_path="anomaly_export.csv"):
    conn = sqlite3.connect(os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "db", "anomalies.db")
    ))
    df = pd.read_sql_query("SELECT * FROM anomalies ORDER BY id DESC", conn)
    conn.close()

    df.to_csv(output_path, index=False)
    print(f"[EXPORT] Anomalies exported to: {output_path}")