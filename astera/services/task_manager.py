import uuid
from uuid import UUID
from astera.models.task import Task
from datetime import timedelta, datetime
from astera.services.database.db_utils import connect_to_db


class TaskManger:

    def add_task(self, task: Task, user_id: int):
        if not isinstance(task, Task):
            raise TypeError("It's not an task object")
        elif not isinstance(user_id, int):
            raise TypeError("User id not int type")

        try:
            connect = connect_to_db()
            if connect is None:
                return None
            with connect.cursor() as cur:
                cur.execute(
                    "INSERT INTO tasks(task_id, title, description, status, creation_date, due_date, user_id)"
                    "VALUES(%s, %s, %s, %s, %s, %s, %s)",
                    (
                        task._id_task,
                        task.title,
                        task.description,
                        task.status,
                        task._creation_date,
                        task.due_date,
                        user_id,
                    ),
                )
                connect.commit()
        except Exception as e:
            if connect:
                print(f"Error to insert data in DB {e}")
                connect.rollback()
        finally:
            if connect:
                connect.close()

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


if __name__ == "__main__":

    try:
        tas1 = Task(
            title="Create documentation",
            description="Write a finance report for Mai",
            due_date=datetime.now() + timedelta(days=7),
            status="To Do"
        )

        manager = TaskManger()
        manager.add_task(task=tas1, user_id=1)
    except Exception as e:
        print(f"Error to insert task1{e}")
    
    task2 = Task(
        title="Check log",
        description="Check log on the server",
        due_date=datetime.now() + timedelta(days=1),
        status="To Do"
    )

    manager.add_task(task=task2, user_id=99)
    
