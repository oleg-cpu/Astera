import uuid
from uuid import UUID
from astera.models.task import Task
from datetime import timedelta, datetime
from astera.services.database.db_utils import connect_to_db


class TaskManager:

    def _execute_query(
        self,
        sql: str,
        parametrization: tuple,
        fetch_one=False,
        commit=False,
    ):
        connect = None
        try:
            connect = connect_to_db()
            if connect is None:
                return None
            with connect.cursor() as cur:
                cur.execute(sql, parametrization)
                if commit is True:
                    if cur.rowcount > 0:
                        connect.commit()
                        return True
                    return False
                elif commit is False and fetch_one is True:
                    return cur.fetchone()
                else:
                    return cur.fetchall()

        except Exception as e:
            if connect:
                print(f"Connect to DB unseccessful{e}")
                connect.rollback()

            if commit:
                return False
            else:
                return None

        finally:
            if connect:
                connect.close()

    def add_task(self, task: Task, user_id: int):
        if not isinstance(task, Task):
            raise TypeError("It's not an task object")
        elif not isinstance(user_id, int):
            raise TypeError("User id not int type")
        return self._execute_query(
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
            commit=True,
        )

    def get_task_by_id(self, id_task: uuid.UUID):
        if not isinstance(id_task, UUID):
            raise TypeError("id_task not object uuid")
        query_result = self._execute_query(
            "SELECT * FROM tasks WHERE task_id =%s",
            (id_task,),
            fetch_one=True,
            commit=False,
        )
        if query_result is None:
            print(f"Task with id {id_task} not found in DB")
            return None
        else:
            return query_result

    def update_task(self, id_task: uuid.UUID, updates: dict):
        if not isinstance(id_task, UUID):
            raise TypeError("id_task not object UUID")
        elif not isinstance(updates, dict):
            raise TypeError("updates not dict object")
        elif not updates:
            print("Updates dict is empty")
            return True

        value_set = []
        update_values = []

        for key, value in updates.items():
            value_set.append(f"{key} = %s")
            update_values.append(value)
        clause_str = ", ".join(value_set)
        full_sql = f"UPDATE tasks SET {clause_str} WHERE task_id = %s"
        final_parameterize_sql = tuple(update_values) + (id_task,)
        return self._execute_query(
            full_sql, final_parameterize_sql, fetch_one=False, commit=True
        )

    def delete_task(self, id_task: uuid.UUID):
        if not isinstance(id_task, uuid.UUID):
            raise TypeError("id_task not object UUID")
        return self._execute_query(
            "DELETE FROM tasks Where task_id =%s",
            (id_task,),
            fetch_one=False,
            commit=True,
        )


if __name__ == "__main__":

    try:
        first_test_task = Task(
            title="Test task",
            description="description for test task",
            due_date=datetime.now() + timedelta(days=7),
            status="To Do",
        )
        print("Add task to DB")
        manager = TaskManager()
        manager.add_task(task=first_test_task, user_id=1)
        print(f"Successful added task to DB {first_test_task}")

        print("Find task in DB")
        existing_task_in_db = first_test_task._id_task
        found_task = manager.get_task_by_id(existing_task_in_db)
        print(f"Successfull found task {found_task}")
    except Exception as e:
        print(f"Error to insert task1{e}")

    second_test_task = Task(
        title="Check log",
        description="Check log on the server",
        due_date=datetime.now() + timedelta(days=1),
        status="To Do",
    )
    print("Find unexisting task in DB")
    manager.add_task(task=second_test_task, user_id=99)
    fake_task_id = uuid.uuid4()
    print(f"Unexisting id {fake_task_id}")
    unexists_task_id = manager.get_task_by_id(fake_task_id)

    update_data = {
        "title": "Update title for test task",
        "status": "Done",
        "description": "Description has been successfully modified.",
    }

    update_status = manager.update_task(existing_task_in_db, update_data)
    print(f"UPDATE status: {update_status}")

    updated_record = manager.get_task_by_id(existing_task_in_db)
    if (
        updated_record
        and updated_record[2] == "Update title for test task"
        and updated_record[5] == "Done"
    ):
        print(
            f"VERIFICATION SUCCESS: New Title is '{updated_record[2]}' and Status is '{updated_record[5]}'"
        )
    else:
        print("VERIFICATION FAILURE: Title or Status was not updated correctly.")

    print("\n--- 5. Testing UPDATE Task (Empty dict) ---")
    empty_update = manager.update_task(existing_task_in_db, {})
    print(f"UPDATE empty dict status: {empty_update}")

    print("\n--- 6. Testing UPDATE Task (Non-existent ID) ---")
    fake_update = manager.update_task(uuid.uuid4(), {"title": "Should Fail"})
    print(f"UPDATE non-existent ID status: {fake_update}")

    print("Testing delete tasks")
    print(f"Delete task with id{existing_task_in_db}")
    delete_sucess = manager.delete_task(existing_task_in_db)
    print(f"delete real status {delete_sucess}")

    delete_failur = manager.delete_task(existing_task_in_db)
    print(f"Unsuccess delete task {delete_failur}")

    print("\n--- All tests completed ---")
