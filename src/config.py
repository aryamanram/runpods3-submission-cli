import os

AWS_REGION      = os.getenv("AWS_REGION", "us-east-1")
S3_BUCKET       = os.getenv("JOB_BUCKET",  "job-artifacts")
S3_ENDPOINT_URL = os.getenv("S3_ENDPOINT_URL")  # leave None for real AWS