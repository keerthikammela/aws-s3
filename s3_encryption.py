# -----------------------server side encryption - s3-------------------------------

import base64
import boto3
from cryptography.fernet import Fernet

s3 = boto3.client('s3')

bucket_name = 'test-bucket'
object_key = 'clientSidEncrypted .txt'
data = 'Confidential information'.encode()

# Upload object with SSE-S3 encryption
s3.put_object(
    Bucket=bucket_name,
    Key=object_key,
    Body=data,
    ServerSideEncryption='AES256'
)

print(f"Uploaded {object_key} with SSE-S3 encryption.")

# -----------------------server side encrption-kms---------------------------------------------------------

kms_key_id = 'arn:aws:kms:us-east-1:123456789012:key/my-key-id' # Your KMS arn 

s3.put_object(
    Bucket=bucket_name,
    Key=object_key,
    Body=data,
    ServerSideEncryption='aws:kms',
    SSEKMSKeyId=kms_key_id
)

print(f"Uploaded {object_key} with SSE-KMS encryption.")

# ------------------------server side encryption with customer provided keys---------------

# Generate a 256-bit (32-byte) encryption key (must be securely stored)
encryption_key = base64.b64encode(b'supersecretkey32byteslong1234')

s3.put_object(
    Bucket=bucket_name,
    Key=object_key,
    Body=data,
    SSECustomerAlgorithm='AES256',
    SSECustomerKey=encryption_key
)

print(f"Uploaded {object_key} with SSE-C encryption.")

# -----------------------------------client side encryption--------------------------------

# Generate encryption key (should be securely stored)
key = Fernet.generate_key()
cipher = Fernet(key)

# Encrypt data
encrypted_data = cipher.encrypt(data)

s3.put_object(
    Bucket=bucket_name,
    Key=object_key,
    Body=encrypted_data
)

print(f"Uploaded {object_key} with Client-Side encryption.")

# Decryption example (Retrieve and decrypt the data)
retrieved_object = s3.get_object(Bucket=bucket_name, Key=object_key)
retrieved_data = retrieved_object['Body'].read()

# Decrypt the data
decrypted_data = cipher.decrypt(retrieved_data).decode()
print("Decrypted Data:", decrypted_data)
