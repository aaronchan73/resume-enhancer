import json
from collections import Counter
import boto3
import os
import urllib.request

EC2_URL = os.getenv("EC2_URL")

def parse_uuid(file_key):
    return file_key.split("_")[0]


def lambda_handler(event, context):
    try:
        s3 = boto3.client("s3")

        # Get bucket name and file key from the S3 event
        print(event)
        bucket_name = event["Records"][0]["s3"]["bucket"]["name"]
        file_key = event["Records"][0]["s3"]["object"]["key"]

        # Get the file object from S3
        resume_obj = s3.get_object(Bucket=bucket_name, Key=file_key)

        # Read the content of the resume file
        resume = resume_obj["Body"].read().decode("utf-8")
        print(f"Content of the file {file_key} from bucket {bucket_name}:", resume)

        resume_id = parse_uuid(file_key)
        print("Resume ID:", resume_id)

        # Read the content of the job description file  
        job_desc_obj = s3.get_object(Bucket=bucket_name, Key=file_key.replace("_resume", "_job_desc"))
        job_desc = job_desc_obj["Body"].read().decode("utf-8")
        print(f"Content of the file {file_key.replace('_resume', '_job_desc')} from bucket {bucket_name}:", job_desc)

        ec2 = boto3.client('ec2')
        instance_info = ec2.describe_instances(InstanceIds=[os.getenv("INSTANCE_ID")])
        public_ip = instance_info['Reservations'][0]['Instances'][0]['PublicIpAddress']

        # Send the resume and job description to the EC2 instance to enhance the resume
        ec2_endpoint = f"http://{public_ip}:5000/enhance/{bucket_name}/{resume_id}"
        print("Calling", ec2_endpoint, "...")

        enhanced_resume = urllib.request.urlopen(ec2_endpoint).read()
        print("Enhanced Resume:", enhanced_resume)

        # Save the enhanced resume to the DynamoDB table
        resume_table = boto3.resource("dynamodb", region_name="ca-central-1").Table(
            "enhanced_resumes"
        )
        data = {
            "resume_id": resume_id,
            "input_resume": resume,
            "input_job_desc": job_desc,
            "enhanced_resume": enhanced_resume,
        }
        resume_table.put_item(Item=data)
       
    except Exception as e:
        print(f"Exception: {e}")
        return {"statusCode": 500, "body": json.dumps({"message ": str(e)})}

    return {"statusCode": 200, "body": data}
