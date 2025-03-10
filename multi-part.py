import boto3

s3_client = boto3.client(
    "s3"
)

# use any file with large data to upload into s3 using multi-part method.

bucket_name = "test-bucket"
file_path = "Tables.txt"
key = "uploaded-large-data-file.txt"  

# decide the file multipart file size based on the sixe of input file.
PART_SIZE = 15*1024*1024 

def multipart_upload():
    try:
        response = s3_client.create_multipart_upload(Bucket=bucket_name, Key=key)
        upload_id = response["UploadId"]

        parts = []
        part_number = 1

        with open(file_path, "rb") as file:
            while chunk := file.read(PART_SIZE):
                part_response = s3_client.upload_part(
                    Bucket=bucket_name,
                    Key=key,
                    PartNumber=part_number,
                    UploadId=upload_id,
                    Body=chunk,
                )
                parts.append({"PartNumber": part_number, "ETag": part_response["ETag"]})
                part_number += 1

        s3_client.complete_multipart_upload(
            Bucket=bucket_name,
            Key=key,
            UploadId=upload_id,
            MultipartUpload={"Parts": parts},
        )

        print(f"File uploaded successfully to s3://{bucket_name}/{key}")

    except Exception as e:
        print(f"Upload failed: {e}")
        s3_client.abort_multipart_upload(Bucket=bucket_name, Key=key, UploadId=upload_id)

multipart_upload()
