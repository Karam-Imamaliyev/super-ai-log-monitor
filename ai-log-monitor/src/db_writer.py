import sqlite3
from typing import Tuple

class AnomalyDatabase:
    def __init__(self, db_path="./db/anomalies.db"):
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
        self.conn.execute(query, (timestamp, level, message, score))
        self.conn.commit()

    def close(self):
        self.conn.close()

import pandas as pd

def export_anomalies_to_csv(db_path, output_path):
    import sqlite3
    conn = sqlite3.connect(db_path)
    query = "SELECT timestamp, level, message, score FROM anomalies"
    df = pd.read_sql_query(query, conn)
    df.to_csv(output_path, index=False)
    conn.close()
