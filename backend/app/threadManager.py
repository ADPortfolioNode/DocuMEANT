from datetime import datetime
import uuid

class Thread:
    def __init__(self, task_description, parent_thread_id=None):
        self.thread_id = f"{str(uuid.uuid4())}"
        self.task_description = task_description
        self.parent_thread_id = parent_thread_id
        self.status = "active"
        self.messages = []
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.completed_at = None
        self.children_threads = []

    def add_message(self, content, sender):
        message = {
            "id": str(uuid.uuid4()),
            "content": content,
            "timestamp": datetime.now(),
            "sender": sender
        }
        self.messages.append(message)
        self.updated_at = datetime.now()

    def complete_thread(self):
        self.status = "completed"
        self.completed_at = datetime.now()
        self.updated_at = datetime.now()

class ThreadManager:
    def __init__(self):
        self.main_thread = None
        self.active_threads = {}

    def create_main_thread(self, task_description="Main Thread"):
        if not self.main_thread:
            self.main_thread = Thread(task_description)
            self.active_threads[self.main_thread.thread_id] = self.main_thread
        return self.main_thread

    def create_sub_thread(self, task_description, parent_thread_id):
        sub_thread = Thread(task_description, parent_thread_id)
        self.active_threads[sub_thread.thread_id] = sub_thread
        return sub_thread

    def get_thread(self, thread_id):
        return self.active_threads.get(thread_id)

    def get_thread_status(self, thread_id):
        thread = self.get_thread(thread_id)
        if thread:
            return {
                "thread_id": thread.thread_id,
                "status": thread.status,
                "task_description": thread.task_description,
                "message_count": len(thread.messages),
                "created_at": thread.created_at,
                "completed_at": thread.completed_at,
                "children_count": len(thread.children_threads)
            }
        return None

    def get_all_active_threads(self):
        return [self.get_thread_status(thread_id) for thread_id in self.active_threads]

    def update_main_thread(self, message):
        if self.main_thread:
            self.main_thread.add_message(message, "system")