from flask import Flask
import requests
import boto3
import pickle

OLLAMA_URL = 'http://localhost:11434/api/generate'

app = Flask(__name__)
s3 = boto3.client('s3')

def load_data(bucket_name, file_name):
    obj = s3.get_object(Bucket=bucket_name, Key=file_name)
    data = obj['Body'].read()
    return pickle.loads(data, encoding='bytes')

@app.route("/enhance/<bucket>/<file>")
def hello_world(bucket, file):
    resume = load_data(bucket, file)
    
    result = requests.get(OLLAMA_URL, json={
        "model": "llama3.2:1b",
        "prompt": "Given this resume: " + resume.decode('utf-8') + ", enhance it.",
        "stream": False
    })

    return result

if __name__ == '__main__':
    app.run()