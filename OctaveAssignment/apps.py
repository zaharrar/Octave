from django.apps import AppConfig
import queue
from .threads import ManagerThread


class MyAppConfig(AppConfig):
    name = "OctaveAssignment"
    task_queue = queue.Queue()

    def ready(self):
        manager = ManagerThread(self.task_queue)
        manager.start()
