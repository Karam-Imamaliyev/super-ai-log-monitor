# src/utils.py

import boto3
import os

def upload_log_to_s3(file_path):
    s3 = boto3.client("s3")
    bucket_name = "super-ai-log-monitor"
    object_name = os.path.basename(file_path)
    try:
        s3.upload_file(file_path, bucket_name, object_name)
        return True, f"Successfully uploaded '{object_name}' to bucket '{bucket_name}'"
    except Exception as e:
        return False, f"Upload failed: {e}"



def get_log_level(score: float) -> str:
    """
    Maps anomaly scores to log severity levels.

    Args:
        score (float): Anomaly score.

    Returns:
        str: One of ["INFO", "WARNING", "ERROR", "CRITICAL"]
    """
    if score < 0.3:
        return "INFO"
    elif score < 0.6:
        return "WARNING"
    elif score < 0.8:
        return "ERROR"
    else:
        return "CRITICAL"
