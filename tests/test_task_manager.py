import unittest
import datetime
import uuid
from astera.models.task import Task
from astera.services.task_manager import TaskManger


class TestTaskManager(unittest.TestCase):
    def setUp(self):
        self.manager = TaskManger()
        self.task1 = Task(
            title="Test1",
            description="Description for test 1",
            due_date=datetime.datetime(2025, 11, 11),
        )
        self.task2 = Task(
            title="Test2",
            description="description for test 2",
            due_date=datetime.datetime(2025, 11, 11),
        )

    def test_add_and_get_task_sucess(self):
        self.manager.add_task(self.task1)
        get_task_by_id = self.manager.get_task(self.task1._id_task)
        self.assertIs(self.task1, get_task_by_id, "not the same")

    def test_get_all_test_sucess(self):
        self.manager.add_task(self.task1)
        self.manager.add_task(self.task2)
        expected_tasks = [self.task1, self.task2]
        get_all_tasks = self.manager.get_all_tasks()
        self.assertCountEqual(expected_tasks, get_all_tasks, "Not equal")

    def test_delete_task_success(self):
        self.manager.add_task(self.task1)
        self.manager.delete_task(self.task1._id_task)
        self.assertEqual(self.manager.get_all_tasks(), [], "task list is empty")

    def test_delete_non_existent_task(self):
        non_exists_task_id = uuid.uuid4()
        with self.assertRaises(KeyError) as cm:
            self.manager.delete_task(non_exists_task_id)
        self.assertEqual(str(cm.exception.args[0]), "The task doesn't exists")

    def test_get_task_not_found(self):
        non_exists_task_id = uuid.uuid4()
        with self.assertRaises(KeyError) as cm:
            self.manager.get_task(non_exists_task_id)
        self.assertEqual(str(cm.exception.args[0]), "The task not in the list")

    def test_get_task_invalid_type(self):
        incorect_task_id = "task_id"
        with self.assertRaises(TypeError) as cm:
            self.manager.get_task(incorect_task_id)
        self.assertEqual(str(cm.exception), "id_task not object uuid")


if __name__ == "__name__":
    unittest.main()
