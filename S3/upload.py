import logging
import boto3
from botocore.exceptions import ClientError
import os
from dotenv import load_dotenv

load_dotenv(".env")

# for key, value in os.environ.items():
    # print(f"{key}: {value}")

def upload_file(file_name, bucket, object_name=None):
    # Verify env file is setup correctly
    print("AWS Access Key:", os.getenv("AWS_ACCESS_KEY_ID"))

    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3', aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"), aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"), aws_session_token=os.getenv("AWS_SESSION_TOKEN"))

    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
        print(response)
    except ClientError as e:
        logging.error(e)
        return False

    return True

bucket_name = os.getenv("BUCKET_NAME")
file_path = os.getenv("FILE_PATH")
upload_file(file_path, bucket_name, 'resume.txt')

