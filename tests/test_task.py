import unittest
import datetime
from datetime import timedelta
from astera.models.task import Task


class TestTask(unittest.TestCase):

    def test_tittle_validation_empty(self):
        with self.assertRaises(ValueError) as cm:
            Task(
                title="",
                description="Description",
                status="To Do",
                due_date=datetime.datetime.now(),
            )
        self.assertEqual(str(cm.exception), "Title can't be empty")

    def test_title_validation_too_long(self):

        with self.assertRaises(ValueError) as cm:
            Task(
                title="S" * 51,
                description="Description",
                status="To Do",
                due_date=datetime.datetime.now(),
            )
        self.assertEqual(str(cm.exception), "Title can't be more than 50 characters")

    def test_description_validation_with_only_spaces(self):
        with self.assertRaises(ValueError) as cm:
            Task(
<<<<<<< HEAD
                title="Test tittle" ,
=======
                title="Test tittle",
>>>>>>> feature/data-base
                description="   ",
                status="To Do",
                due_date=datetime.datetime.now(),
            )
        self.assertEqual(
            str(cm.exception), "Description can contain only characters not just spaces"
        )

    def test_description_validation_to_long(self):
        with self.assertRaises(ValueError) as cm:
            Task(
                title="Test tittle",
                description="Description" * 501,
                status="To Do",
                due_date=datetime.datetime.now(),
            )
        self.assertEqual(
            str(cm.exception), "Description can't be more than 500 characters"
        )

    def test_set_empty_status(self):
        with self.assertRaises(ValueError) as cm:
            Task(
                title="Test title",
                description="Description",
                status="",
                due_date=datetime.datetime.now(),
            )
        self.assertEqual(str(cm.exception), "Status can't be empty")

    def test_status_validation_invalid_setter(self):
        task_object = Task(
            title="Test tittle",
            description="Description",
            status="To Do",
            due_date=datetime.datetime(2025, 11, 11),
        )
        with self.assertRaises(ValueError) as cm:
            task_object.status = "Invalid"
        self.assertEqual(str(cm.exception), "Status doesn't exists")

    def test_due_date_incorrect_format(self):
        with self.assertRaises(TypeError) as cm:
            Task(
                title="Test title",
                description="Description",
                status="To Do",
                due_date="datetime",
            )
        self.assertEqual(str(cm.exception), "incorrect format date and time")

    def test_due_date_validation_past(self):
        priviuse_date = datetime.datetime.now() - timedelta(days=1)
        with self.assertRaises(ValueError) as cm:
            Task(
                title="Test title",
                description="Description",
                status="To Do",
                due_date=priviuse_date,
            )
        self.assertEqual(str(cm.exception), "Due date cannot be in the past")

    def test_to_dict_conversion(self):
        task_object = Task(
            title="Test title",
            description="Description",
            status="To Do",
            due_date=datetime.datetime(2050, 11, 11),
        )
        actual_dict = task_object.to_dict()
        expected_dict = {
            "id_task": str(task_object._id_task),
            "title": "Test title",
            "description": "Description",
            "status": "To Do",
            "creation_date": str(task_object._creation_date),
<<<<<<< HEAD
            "due_date": str(datetime.datetime(2050, 11 ,11)),
=======
            "due_date": str(datetime.datetime(2050, 11, 11)),
>>>>>>> feature/data-base
        }

        self.assertIsInstance(task_object.to_dict(), dict, "Must return dict type")
        self.assertEqual(actual_dict, expected_dict, "Dict must have the same values")
