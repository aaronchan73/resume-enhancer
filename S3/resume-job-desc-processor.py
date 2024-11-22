import json
from collections import Counter
import boto3


def lambda_handler(event, context):
    try:
        s3 = boto3.client("s3")

        # Get bucket name and file key from the S3 event
        print(event)
        bucket_name = event["Records"][0]["s3"]["bucket"]["name"]
        file_key = event["Records"][0]["s3"]["object"]["key"]

        # Get the file object from S3
        file_obj = s3.get_object(Bucket=bucket_name, Key=file_key)

        # Read the content of the file
        file_content = file_obj["Body"].read().decode("utf-8")

        print(f"Content of the file {file_key} from bucket {bucket_name}:")

        resume_id = ""
        input_resume = ""
        input_job_desc = ""

        # TODO: Call REST API on the ec2 server and get the returned enhanced resume

        enhanced_resume = ""

        resume_table = boto3.resource("dynamodb", region_name="ca-central-1").Table(
            "enhanced_resumes"
        )
        data = {
            "resume_id": resume_id,
            "input_resume": input_resume,
            "input_job_desc": input_job_desc,
            "enhanced_resume": enhanced_resume,
        }
    except Exception as e:
        print(f"Exception: {e}")
        return {"statusCode": 500, "body": json.dumps({"message ": str(e)})}

    return {"statusCode": 200, "body": str(sorted_word_count)}
