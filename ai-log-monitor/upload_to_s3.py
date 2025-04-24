import boto3
import os

#  CONFIGURATION
BUCKET_NAME = "super-ai-log-monitor"  # bucket - we created
FILE_PATH = "data/mylog.log"         # document - we want to install
OBJECT_NAME = os.path.basename(FILE_PATH)  # the name in s3 (will be same)

def upload_file():
    s3 = boto3.client('s3')
    try:
        s3.upload_file(FILE_PATH, BUCKET_NAME, OBJECT_NAME)
        print(f"Successfully uploaded '{FILE_PATH}' to bucket '{BUCKET_NAME}'")
    except Exception as e:
        print(f" Upload failed: {e}")

if __name__ == "__main__":
    upload_file()
