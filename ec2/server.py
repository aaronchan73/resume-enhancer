from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    # http://localhost:11434/api/generate -d '{
    #   "model": "llama3.2",
    #   "prompt": "Why is the sky blue?",
    #   "stream": false
    # }'
    return "Hello World"

if __name__ == '__main__':
    app.run()