import boto3
import requests

bucket = "test-bucket"
key = "example.txt"

s3 = boto3.client('s3')

url = s3.generate_presigned_url('get_object',
                                Params={'Bucket': bucket, 'Key': key},
                                ExpiresIn=3600) 

print(url)

key = "samplefile.txt"

upload_url = s3.generate_presigned_url(
    'put_object',
    Params={'Bucket': bucket, 'Key': key},
    ExpiresIn=600
)

print("Upload URL:", upload_url)

file_path = 'myfile.txt'  # Local file to upload
with open(file_path, 'rb') as file:
    response = requests.put(upload_url, data=file)
    print(response.status_code)  # 200 means success


