import os
import boto3
import requests

# Get environment variables
AWS_KEY = os.getenv('AWS_KEY')
AWS_SECRET = os.environ.get('AWS_SECRET')

OBJECT_FILE = "82739657/C1_S9_L001_R1_001.fastq.gz"

s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_KEY,
    aws_secret_access_key=AWS_SECRET
)

# Generate the presigned URL
response = s3_client.generate_presigned_post(
    Bucket='presigned-uploader',
    Key=OBJECT_FILE,
    ExpiresIn=10
)

print(response)

# Upload file to s3 using presigned URL
files = {'file': open(OBJECT_FILE, 'rb')}
r = requests.post(response['url'], data=response['fields'], files=files)
print(r.status_code)
