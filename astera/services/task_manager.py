import uuid
from uuid import UUID
from astera.models.task import Task


class TaskManger:
    _tasks = {}

    def __init__(self, tasks: dict = None):
        if tasks is None:
            self._tasks = {}
        else:
            self._tasks = tasks.copy()

    def add_task(self, task: Task):
        if not isinstance(task, Task):
            raise TypeError("It's not Task Object")
        else:
            self._tasks[task._id_task] = task

    def get_task(self, id_task: uuid.UUID):
        if not isinstance(id_task, UUID):
            raise TypeError("id_task not object uuid")
        elif id_task not in self._tasks:
            raise KeyError("The task not in the list")
        else:
            return self._tasks[id_task]

    def delete_task(self, id_task: uuid.UUID):
        if not isinstance(id_task, UUID):
            raise TypeError("id_task not object uuid")
        elif id_task not in self._tasks:
            raise KeyError("The task doesn't exists")
        else:
            deleted_task = self._tasks.pop(id_task)
            return deleted_task

    def get_all_tasks(self):
        all_tasks = []
        all_tasks = self._tasks.values()
        sorted_tasks_by_date = sorted(
            all_tasks, key=lambda task: task._creation_date, reverse=True
        )
        return sorted_tasks_by_date
