from flask import Flask, request, jsonify
from flask_cors import CORS
from app.threadManager import ThreadManager  # Ensure the correct import path

app = Flask(__name__)
CORS(app)

thread_manager = ThreadManager()
main_thread = thread_manager.create_main_thread()

@app.route('/api/threads', methods=['GET'])
def get_threads():
    return jsonify(thread_manager.get_all_active_threads())

@app.route('/api/threads', methods=['POST'])
def create_thread():
    data = request.json
    task_description = data.get('task_description')
    parent_thread_id = data.get('parent_thread_id')
    if parent_thread_id:
        thread = thread_manager.create_sub_thread(task_description, parent_thread_id)
    else:
        thread = thread_manager.create_main_thread(task_description)
    return jsonify(thread.__dict__)

@app.route('/api/threads/<thread_id>', methods=['GET'])
def get_thread(thread_id):
    thread = thread_manager.get_thread(thread_id)
    if thread:
        return jsonify(thread.__dict__)
    return jsonify({"error": "Thread not found"}), 404

@app.route('/api/threads/<thread_id>/messages', methods=['GET'])
def get_thread_messages(thread_id):
    thread = thread_manager.get_thread(thread_id)
    if thread:
        return jsonify(thread.messages)
    return jsonify({"error": "Thread not found"}), 404

@app.route('/api/threads/<thread_id>/messages', methods=['POST'])
def add_thread_message(thread_id):
    data = request.json
    content = data.get('content')
    sender = data.get('sender')
    thread = thread_manager.get_thread(thread_id)
    if thread:
        thread.add_message(content, sender)
        if thread.parent_thread_id:
            parent_thread = thread_manager.get_thread(thread.parent_thread_id)
            if parent_thread:
                parent_thread.add_message(content, sender)
        return jsonify(thread.messages)
    return jsonify({"error": "Thread not found"}), 404

@app.route('/api/threads/<thread_id>/complete', methods=['POST'])
def complete_thread(thread_id):
    thread = thread_manager.get_thread(thread_id)
    if thread:
        thread.complete_thread()
        return jsonify(thread.__dict__)
    return jsonify({"error": "Thread not found"}), 404

@app.route('/api/threads/<thread_id>/children', methods=['GET'])
def get_thread_children(thread_id):
    thread = thread_manager.get_thread(thread_id)
    if thread:
        children = [thread_manager.get_thread(child_id).__dict__ for child_id in thread.children_threads]
        return jsonify(children)
    return jsonify({"error": "Thread not found"}), 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)