import boto3
import botocore

# Create an S3 client with specified region
s3 = boto3.client("s3", region_name="eu-central-1", config=botocore.config.Config(connect_timeout=5, read_timeout=5))

try:
    # List all buckets
    response = s3.list_buckets()
    print("✅ Your S3 Buckets:")
    for bucket in response["Buckets"]:
        print(" -", bucket["Name"])
except Exception as e:
    print("❌ Error:", e)
