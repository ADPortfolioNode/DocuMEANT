from flask import Flask, jsonify, request
from flask_cors import CORS
from app.threadManager import ThreadManager

app = Flask(__name__)
CORS(app)

# Initialize ThreadManager
thread_manager = ThreadManager()
main_thread = thread_manager.create_main_thread()

@app.route('/')
def hello():
    return "Hello, World!"

@app.route('/api/status')
def status():
    return {"message": "Backend is running"}

@app.route('/api/chromadb/status')
def chromadb_status():
    return {"message": "ChromaDB is running"}

# New endpoints for thread management
@app.route('/api/threads', methods=['GET'])
def get_threads():
    active_threads = thread_manager.get_all_active_threads()
    return jsonify(active_threads)

@app.route('/api/threads', methods=['POST'])
def create_thread():
    data = request.json
    task_description = data.get('task_description')
    parent_thread_id = data.get('parent_thread_id')
    
    new_thread = thread_manager.create_sub_thread(task_description, parent_thread_id)
    return jsonify(thread_manager.get_thread_status(new_thread.thread_id))

@app.route('/api/threads/<thread_id>', methods=['GET'])
def get_thread(thread_id):
    thread_status = thread_manager.get_thread_status(thread_id)
    if thread_status:
        return jsonify(thread_status)
    return jsonify({"error": "Thread not found"}), 404

if __name__ == "__main__":
    app.run(host='0.0.0.0')