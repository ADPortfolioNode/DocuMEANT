from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello():
    return "Hello, World!"

@app.route('/api/status')
def status():
    return {"message": "Backend is running"}

@app.route('/api/chromadb/status')
def chromadb_status():
    return {"message": "ChromaDB is running"}

if __name__ == "__main__":
    app.run(host='0.0.0.0')