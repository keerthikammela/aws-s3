import boto3

s3_client = boto3.client(
    "s3"
)

bucket_name = "test-bucket"
file_path = "path/example.txt" 
s3_key = "uploaded-file.txt" 

try:
    s3_client.upload_file(file_path, bucket_name, s3_key)
    print(f"File uploaded successfully to s3://{bucket_name}/{s3_key}")
except Exception as e:
    print(f"File upload failed: {e}")
