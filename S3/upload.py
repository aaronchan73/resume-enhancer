import boto3
import logging
import os
import time
import uuid
from botocore.exceptions import ClientError
from dotenv import load_dotenv

load_dotenv()

TABLE_NAME = "enhanced_resumes"
PARTITION_KEY = "resume_id"
POLL_INTERVAL = 5  # Seconds between polls

bucket_name = os.getenv("BUCKET_NAME")

# for key, value in os.environ.items():
# print(f"{key}: {value}")

dynamodb = boto3.resource(
    "dynamodb",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    aws_session_token=os.getenv("AWS_SESSION_TOKEN"),
)
table = dynamodb.Table(TABLE_NAME)

s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    aws_session_token=os.getenv("AWS_SESSION_TOKEN"),
)


def upload_file(resume_file_name, job_desc_file_name, bucket):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    # Generate a unique resume_id using UUID
    resume_id = str(uuid.uuid4())

    # Upload the file
    try:
        s3_client.upload_file(
            job_desc_file_name, bucket, f"{resume_id}_job_desc.txt"
        )
        s3_client.upload_file(
            resume_file_name, bucket, f"{resume_id}_resume.txt"
        )
    except ClientError as e:
        logging.error(e)
        return -1

    return resume_id


def get_item(key_name, key_value):
    try:
        response = table.get_item(Key={key_name: key_value})
        print("Item retrieved from DynamoDB:", response)
        return response.get("Item", None)
    except ClientError as e:
        print(f"Error fetching item: {e.response['Error']['Message']}")
        return None


def poll_for_updated_resume(key_name, key_value, interval):
    print(f"Polling DynamoDB table '{TABLE_NAME}' for item with key '{key_value}'...")

    while True:
        item = get_item(key_name, key_value)

        if item:
            print(f"Item found: {item}")
            return "Item" in item
        else:
            print("Item not found. Retrying...")

        time.sleep(interval)


if __name__ == "__main__":
    print("Bucket name:", bucket_name)

    resume_file_name = "resume.txt"
    job_desc_file_name = "job_desc.txt"

    resume_id = upload_file(resume_file_name, job_desc_file_name, bucket_name)
    print("Resume successfully uploaded with id", resume_id)

    resume_row = poll_for_updated_resume(PARTITION_KEY, resume_file_name, POLL_INTERVAL)
    print("Resume row:", resume_row)
    if resume_row and "enhanced_resume" in resume_row:
        with open("enhanced_resume.txt", "w") as file:
            file.write(resume_row["enhanced_resume"])
        print("Enhanced resume saved to enhanced_resume.txt")
    else:
        print("Enhanced resume not found in the database.")
