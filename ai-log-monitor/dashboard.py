import os
import sqlite3
import pandas as pd
import streamlit as st
from src.utils import upload_log_to_s3


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "db", "anomalies.db")
LOG_PATH = os.path.join(BASE_DIR, "data", "mylog.log")
BUTTON_LOG_PATH = os.path.join(BASE_DIR, "data", "mylog_button.log")


@st.cache_data
def fetch_anomalies():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM anomalies ORDER BY id DESC", conn)
    conn.close()
    return df

st.title("AI Log Anomaly Dashboard")

df = fetch_anomalies()
st.dataframe(df, use_container_width=True)

if st.button(" Upload log to S3"):
    success, message = upload_log_to_s3(file_path=BUTTON_LOG_PATH)
    if success:
        st.success(message)
    else:
        st.error(message)

st.markdown("## Log Details")

selected = st.selectbox("Select a log for details:", df["message"] if not df.empty else [])

if selected:
    selected_row = df[df["message"] == selected].iloc[0]
    st.code(f"""
Timestamp : {selected_row['timestamp']}
Level     : {selected_row['level']}
Score     : {selected_row['score']:.2f}
Message   : {selected_row['message']}
""", language="yaml")
