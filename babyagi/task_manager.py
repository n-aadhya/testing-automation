class Task:
    def __init__(self, task_type, payload):
        self.task_type = task_type
        self.payload = payload


class TaskManager:
    def __init__(self):
        self.queue = []

    def add_task(self, task):
        self.queue.append(task)

    def get_next_task(self):
        return self.queue.pop(0) if self.queue else None
