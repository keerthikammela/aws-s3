import boto3

s3 = boto3.client('s3')

bucket_name = 'test-bucket'
object_key = 'large-file.txt'

# Read the first 1024 bytes (1 KB) from the file
response = s3.get_object(Bucket=bucket_name, Key=object_key, Range='bytes=0-1023')

# Get the content from the response
partial_content = response['Body'].read()

print(partial_content.decode())  # Decode if it's text data
