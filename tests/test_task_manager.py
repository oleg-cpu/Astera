import uuid
from datetime import datetime, timedelta
import unittest
from unittest.mock import  patch
from astera.models.task import Task
from astera.services.task_manager import TaskManager


class TestTaskManager(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.manager = TaskManager()

    def setUp(self):
        self.test_task = Task(
            title="Testing task class",
            description="descriptio for class Test",
            status="To Do",
            due_date=datetime.now() + timedelta(days=7),
        )
        self.test_task._id_task = uuid.UUID("00000000-0000-0000-0000-000000000001")
        self.empty_task_title = ""
        self.incorrect_task_status = "Incorrect status"

    @patch("astera.services.task_manager.TaskManager._execute_query")
    def test_add_task_success(self, mock_execute_query):
        test_user_id = 1
        self.manager.add_task(self.test_task, user_id=test_user_id)

        mock_execute_query.assert_called_once()
        call_args = mock_execute_query.call_args[0]
        sql_query = call_args[0]
        parameters = call_args[1]
        self.assertTrue(
            sql_query.strip().startswith("INSERT INTO tasks"),
            "SQL query must start with 'INSERT INTO tasks'",
        )
        self.assertEqual(
            parameters[-1], test_user_id, "Last parameter (user_id) must be correct"
        )

    @patch("astera.services.task_manager.TaskManager._execute_query")
    def test_add_task_incorrect_data(self, mock_execute_query):

        with self.assertRaisesRegex(TypeError, "It's not an task object"):
            self.manager.add_task(task= "Not task object", user_id=1)

        with self.assertRaisesRegex(TypeError, "User id not int type"):
            self.manager.add_task(task=self.test_task, user_id="One")

        mock_execute_query.assert_not_called()

    @patch("astera.services.task_manager.TaskManager._execute_query")
    def test_get_task_by_id_success(self, mock_execute_query):

        expected_result = (
            self.test_task._id_task,
            self.test_task.title,
            self.test_task.description,
            self.test_task.status,
            self.test_task._creation_date,
            self.test_task.due_date
        )
        mock_execute_query.return_value = expected_result
        actual_result = self.manager.get_task_by_id(self.test_task._id_task)
        self.assertEqual(actual_result, expected_result, "Must have the same task") 

        mock_execute_query.assert_called_once()

        positional_args = mock_execute_query.call_args[0]
        sql = positional_args[0]
        parameters = positional_args[1]

        keyword_args = mock_execute_query.call_args[1]
        fetch_one = keyword_args.get("fetch_one")
        commit = keyword_args.get("commit")

        self.assertTrue(sql.strip().startswith("SELECT * FROM tasks WHERE task_id =%s"))
        self.assertEqual(parameters, (self.test_task._id_task,), "ID must be a parameter")
        self.assertTrue(fetch_one, "Must use fetch_one=True")
        self.assertFalse(commit, "Must use commit=False для SELECT")

    @patch("astera.services.task_manager.TaskManager._execute_query")
    def test_get_task_by_id_not_found(self, mock_execute_query):
        mock_execute_query.return_value = None
        incorrect_task_id = uuid.uuid4()
        actual_result = self.manager.get_task_by_id(incorrect_task_id)
        self.assertIsNone(actual_result, "Must be returned None if task unexists")
        mock_execute_query.assert_called_once()

        positional_args = mock_execute_query.call_args[0]
        sql =positional_args[0]
        parameters = positional_args[1]

        self.assertTrue(sql.strip().startswith("SELECT * FROM tasks"))
        self.assertEqual(parameters, (incorrect_task_id,), "ID parameter must be used")

    def test_get_task_by_id_type_error(self):
        with self.assertRaisesRegex(TypeError, "id_task not object uuid"):
            self.manager.get_task_by_id("This a string not a UUID")

    @patch("astera.services.task_manager.TaskManager._execute_query")
    def test_update_task_success(self, mock_execute_query):
        updates = {
            "title": "Success update",
            "description": "Description for success update",
            "status": "To Do",
            "creation_date": datetime.now().replace(microsecond=0),
            "due_date": (datetime.now() + timedelta(days=1)).replace(microsecond=0)
        }

        expected_params = (
            updates["title"],
            updates["description"],
            updates["status"],
            updates["creation_date"],
            updates["due_date"],
            self.test_task._id_task
        )

        mock_execute_query.return_value = True
        actual_result = self.manager.update_task(self.test_task._id_task, updates)
        self.assertTrue(actual_result, "Must return True")

        mock_execute_query.assert_called_once()
        postional_args = mock_execute_query.call_args[0]
        sql = postional_args[0]
        parameters = postional_args[1]

        keyword_args = mock_execute_query.call_args[1]
        commit = keyword_args.get("commit")

        self.assertTrue(
            sql.strip().startswith("UPDATE tasks SET"), "SQL must be update query"
        )
        self.assertIn("title = %s", sql)
        self.assertIn("description = %s", sql)
        self.assertIn("status = %s", sql)
        self.assertIn("creation_date = %s", sql)
        self.assertIn("due_date = %s", sql)
        self.assertTrue(sql.strip().endswith("WHERE task_id = %s"))

        self.assertEqual(parameters, expected_params, "Parameters incorrect")
        self.assertTrue(commit, "must use commit=True for update")

    def test_update_task_incorrect(self):
        with self.assertRaisesRegex(TypeError, "id_task not object UUID"):
            self.manager.update_task("Not a uuid object", {"title": "test title"})

        with self.assertRaisesRegex(TypeError, "updates not dict object"):
            self.manager.update_task(self.test_task._id_task, "Not a dict")

    @patch("astera.services.task_manager.TaskManager._execute_query")
    def test_delete_task_success(self, mock_execute_query):
        mock_execute_query.return_value = True
        task_id_to_delete = self.test_task._id_task
        actual_result = self.manager.delete_task(task_id_to_delete)
        self.assertTrue(actual_result, "Must return True")

        mock_execute_query.assert_called_once()
        positional_args = mock_execute_query.call_args[0]
        sql = positional_args[0]
        parameters = positional_args[1]
        keyword_args = mock_execute_query.call_args[1]
        commit = keyword_args.get("commit")

        self.assertTrue(
            sql.strip().startswith("DELETE FROM tasks"),
            "SQL must be DELETE (should start with 'DELETE FROM tasks')",
        )
        self.assertIn("Where task_id =%s", sql)

        self.assertEqual(
            parameters, (task_id_to_delete,), "Parametr must be task ID"
        )
        self.assertTrue(commit, "Must use commit=True для DELETE")

    def test_delete_task_incorrect(self):
        with self.assertRaisesRegex(TypeError, "id_task not object UUID"):
            self.manager.delete_task("not-a-uuid-string")

if __name__ == "__main__":
    unittest.main()
