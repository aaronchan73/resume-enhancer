1. Ensure .env file is set up with AWS credentials  

2. Run Ollama container
```
docker run -p 11434:11434 tiny-llama-model
```

3. Run EC2 instance
```
python server.py
```

4. Test the EC2 instance
```
curl -X GET "http://127.0.0.1:5000/enhance/resume-job-descriptions/0dfd7f19-34d2-4db1-b15b-808ba19c7c21"
```
