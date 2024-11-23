from flask import Flask
import requests
import os
import boto3
from dotenv import load_dotenv

load_dotenv()

OLLAMA_URL = "http://localhost:11434/api/generate"

app = Flask(__name__)
s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    aws_session_token=os.getenv("AWS_SESSION_TOKEN"),
)


def load_data(bucket_name, file_name):
    obj = s3.get_object(Bucket=bucket_name, Key=file_name)
    data = obj["Body"].read()
    return data.decode("utf-8")


@app.route("/enhance/<bucket>/<id>", methods=["GET"])
def enhance_resume(bucket, id):
    print("Bucket:", bucket, "ID:", id)

    resume = load_data(bucket, id + "_resume.txt")
    job_desc = load_data(bucket, id + "_job_desc.txt")
    print("Resume:", resume)
    print("Job description:", job_desc)

    ollama_body = {
        "model": "tinyllama",
        "prompt": "Given the following resume and job description, enhance the resume to match the job description: "
        + resume
        + "\n\n"
        + job_desc,
        "stream": False,
    }
    print("Ollama body:", ollama_body)

    result = requests.post(OLLAMA_URL, json=ollama_body)
    print("Enhanced resume:", result.json())

    return result.json()["response"]


if __name__ == "__main__":
    app.run(debug=True)
