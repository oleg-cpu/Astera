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

    def get_task_by_id(self, id_task: uuid.UUID):
        if not isinstance(id_task, UUID):
            raise TypeError("id_task not object uuid")
        try:
            connect = connect_to_db()
            if connect is None:
                return None
            with connect.cursor() as cur:
                cur.execute(
                    "SELECT * FROM tasks WHERE task_id =%s", (id_task,) 
                )
                task_record = cur.fetchone()
                if task_record is None:
                    print(f"Task with id {id_task} not found in DB")
                    return None
                return task_record

        except Exception as e:
            if connect:
                print(f"Error to connect DB to get task {e}")
                connect.rollback()
        finally:
            if connect:
                connect.close()

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

        try:
            connect = connect_to_db()
            if connect is None:
                return False
            with connect.cursor() as cur:
                cur.execute(
                    full_sql, final_parameterize_sql
                )
                connect.commit()
                return True
        except Exception as e:
            if connect:
                print(f"Can't update task {e}")
                connect.rollback()
        finally:
            if connect:
                connect.close()

    def delete_task(self, id_task: uuid.UUID):
        if not isinstance(id_task, uuid.UUID):
            raise TypeError("id_task not object UUID")
        
        try:
            connect = connect_to_db()
            if connect is None:
                return False
            with connect.cursor() as cur:
                cur.execute(
                    "DELETE FROM tasks Where task_id =%s", (id_task,)
                )
                if cur.rowcount >= 1:
                    connect.commit()
                    return True
                else:
                    return False
                
        except Exception as e:
            if connect:
                print(f"Cann't delete record from DB {e}")
                connect.rollback()
        finally:
            if connect:
                connect.close()    


if __name__ == "__main__":

    try:
        task1 = Task(
            title="Create documentation",
            description="Write a finance report for Mai",
            due_date=datetime.now() + timedelta(days=7),
            status="To Do"
        )

        manager = TaskManger()
        manager.add_task(task=task1, user_id=1)
        real_task = task1._id_task
        found_task = manager.get_task_by_id(real_task)
        print(f"Successfull found task {found_task}")
    except Exception as e:
        print(f"Error to insert task1{e}")

    task2 = Task(
        title="Check log",
        description="Check log on the server",
        due_date=datetime.now() + timedelta(days=1),
        status="To Do"
    )

    manager.add_task(task=task2, user_id=99)
    fake_task_id = uuid.uuid4()
    unexists_task_id = manager.get_task_by_id(fake_task_id)
    print(unexists_task_id)

    update_data = {
        "title": "New Title After Update",
        "status": "Done",
        "description": "Description has been successfully modified.",
    }

    update_status = manager.update_task(real_task, update_data)
    print(f"UPDATE status: {update_status}")

    updated_record = manager.get_task_by_id(real_task)
    if (
        updated_record
        and updated_record[2] == "New Title After Update"
        and updated_record[5] == "Done"
    ):
        print(
            f"VERIFICATION SUCCESS: New Title is '{updated_record[2]}' and Status is '{updated_record[5]}'"
        )
    else:
        print("VERIFICATION FAILURE: Title or Status was not updated correctly.")

    print("\n--- 5. Testing UPDATE Task (Empty dict) ---")
    empty_update = manager.update_task(real_task, {})
    print(f"UPDATE empty dict status: {empty_update}")

    print("\n--- 6. Testing UPDATE Task (Non-existent ID) ---")
    fake_update = manager.update_task(uuid.uuid4(), {"title": "Should Fail"})
    print(f"UPDATE non-existent ID status: {fake_update}")

    print("Testing delete tasks")
    print(f"Delete task with id{real_task}")
    delete_sucess = manager.delete_task(real_task)
    print(f"delete real status {delete_sucess}")

    delete_failur = manager.delete_task(real_task)
    print(f"Unsuccess delete task {delete_failur}")

    unexisting_task = manager.get_task_by_id(real_task)
    print(unexisting_task)

    print("\n--- All tests completed ---")
