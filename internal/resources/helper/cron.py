import uuid
import schedule
import time
from datetime import datetime
from internal.resources.helper.logger import LoggerManager


class Cron:
    def __init__(self, name, tasks):
        self.name = name
        self.logger = LoggerManager(name)
        self.tasks = tasks
        self.scheduled_tasks = []

    def add_task(self, name, schedule_time, task_function, **kwargs):
        task_id = str(uuid.uuid4())
        task = {
            'id': task_id,
            'name': name,
            'schedule_time': schedule_time,
            'task_function': task_function,
            'kwargs': kwargs
        }
        self.tasks.append(task)
        self.logger.info(f"Task added: {task}")
        return task_id

    def remove_task(self, task_id):
        self.tasks = [task for task in self.tasks if task['id'] != task_id]
        self.logger.info(f"Task removed: {task_id}")

    def schedule_tasks(self):
        for task in self.tasks:
            self.logger.info(f"Scheduling task: {task['name']} at {task['schedule_time']}")
            schedule.every().day.at(task['schedule_time']).do(self.run_task, task)

    def run_task(self, task):
        self.logger.info(f"Running task: {task['name']} at {datetime.now().isoformat()}")
        try:
            task['task_function'](**task['kwargs'])
            self.logger.info(f"Task completed: {task['name']}")
        except Exception as e:
            self.logger.error(f"Task failed: {task['name']} with error {str(e)}")

    def start(self):
        self.logger.info(f"Starting Cron Manager: {self.name}")
        self.schedule_tasks()
        while True:
            schedule.run_pending()
            time.sleep(1)