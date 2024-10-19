from datetime import datetime
import uuid

class Thread:
    def __init__(self, task_description, parent_thread_id=None):
        self.thread_id = f"{datetime.now().strftime('%f')}"  # last 6 digits of microseconds
        self.task_description = task_description
        self.parent_thread_id = parent_thread_id
        self.status = "active"
        self.messages = []
        self.created_at = datetime.now()
        self.completed_at = None
        self.children_threads = []

    def add_message(self, content, sender):
        message = {
            "id": str(uuid.uuid4()),
            "content": content,
            "sender": sender,
            "timestamp": datetime.now()
        }
        self.messages.append(message)
        return message

    def complete_thread(self):
        self.status = "completed"
        self.completed_at = datetime.now()

class ThreadManager:
    def __init__(self):
        self.main_thread = None
        self.active_threads = {}

    def create_main_thread(self):
        if not self.main_thread:
            self.main_thread = Thread("Main System Thread")
            self.active_threads[self.main_thread.thread_id] = self.main_thread
            return self.main_thread
        return self.main_thread

    def create_sub_thread(self, task_description, parent_thread_id):
        new_thread = Thread(task_description, parent_thread_id)
        self.active_threads[new_thread.thread_id] = new_thread
        
        # Add to parent's children if parent exists
        if parent_thread_id in self.active_threads:
            self.active_threads[parent_thread_id].children_threads.append(new_thread.thread_id)
        
        return new_thread

    def get_thread(self, thread_id):
        return self.active_threads.get(thread_id)

    def get_thread_status(self, thread_id):
        thread = self.get_thread(thread_id)
        if thread:
            return {
                "thread_id": thread.thread_id,
                "status": thread.status,
                "task": thread.task_description,
                "message_count": len(thread.messages),
                "created_at": thread.created_at,
                "completed_at": thread.completed_at,
                "children_count": len(thread.children_threads)
            }
        return None

    def get_all_active_threads(self):
        return {
            thread_id: self.get_thread_status(thread_id)
            for thread_id, thread in self.active_threads.items()
            if thread.status == "active"
        }