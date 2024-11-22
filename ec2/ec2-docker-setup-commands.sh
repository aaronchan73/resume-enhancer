docker pull ollama/ollama
docker run -d --name ollama -p 11434:11434 ollama/ollama
docker exec -it ollama ollama run llama3.2:1b
curl http://localhost:11434/api/generate -d '{"model":"llama3.2:1b","prompt":"Why is the sky blue?", "stream": false}'

docker start d2a556f0fab2