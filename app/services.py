class TaskService:
    def __init__(self):
        self.tasks = []
        self.next_id = 1

    def get_all_tasks(self):
        """Retrieve all tasks."""
        return self.tasks

    def create_task(self, title):
        """Create a new task."""
        task = {'id': self.next_id, 'title': title, 'done': False}
        self.next_id += 1
        self.tasks.append(task)
        return task

    def get_task(self, task_id):
        """Get a task by ID. Returns None if not found."""
        return next((t for t in self.tasks if t['id'] == task_id), None)

    def update_task(self, task_id, done):
        """Update task completion status."""
        task = self.get_task(task_id)
        if not task:
            return None
        task['done'] = done
        return task

    def delete_task(self, task_id):
        """Delete a task by ID."""
        task = self.get_task(task_id)
        if not task:
            return False
        self.tasks.remove(task)
        return True
