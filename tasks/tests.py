from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from tasks.models import Task


class TaskViewTest(TestCase):
    def setUp(self):
        User_model = get_user_model()
        self.user = User_model.objects.create_user(username="testUser", password="Password123")

        self.list_url = reverse("task-list")
        self.create_url = reverse("create-task")

        self.test_task = Task.objects.create(
            title="test task",
            description="Description for test task",
            status="To Do",
            due_date=date.today() + timedelta(days=7),
            user_id=self.user,
        )
        self.detail_url = reverse("task-detail", kwargs={"pk": self.test_task.pk})
        self.update_url = reverse("task-update", kwargs={"pk": self.test_task.pk})
        self.delete_url = reverse("task-delete", kwargs={"pk": self.test_task.pk})

    def test_task_list_view_authenticated(self):
        self.client.login(username="testUser", password="Password123")
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.test_task, response.context["object_list"])

    def test_task_list_redirects_unauthenticated_user(self):
        response = self.client.get(self.list_url)
        expected_url = f"/accounts/login/?next={self.list_url}"
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url)

    def test_task_create_view(self):
        self.assertEqual(Task.objects.count(), 1)
        self.client.login(username="testUser", password="Password123")
        future_date = date.today() + timedelta(days=7)
        form_data = {
            "title": "create test task",
            "description": "description for create test task",
            "status": "To Do",
            "due_date": future_date.strftime("%Y-%m-%d"),
        }
        response = self.client.post(self.create_url, data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.list_url)
        self.assertEqual(Task.objects.count(), 2)
        new_task = Task.objects.get(title="create test task")
        self.assertEqual(new_task.user_id, self.user)

    def test_task_create_prevents_past_due_date(self):
        """Test that attempting to create a task with a past due_date fails validation."""
        self.client.login(username="testUser", password="Password123")
        past_date = date.today() - timedelta(days=1)

        form_data = {
            "title": "Invalid Past Date Task",
            "description": "This task should fail validation.",
            "status": "To Do",
            "due_date": past_date.strftime("%Y-%m-%d"),
        }

        response = self.client.post(self.create_url, data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response.context["form"],
            "due_date",
            "The end date cannot be in the past. Please select today's date or a future date.",
        )
        self.assertEqual(Task.objects.count(), 1)

    def test_task_update_prevents_past_due_date(self):

        self.client.login(username="testUser", password="Password123")
        past_date = date.today() - timedelta(days=1)

        invalid_update_data = {
            "title": "Attempted Invalid Update",
            "description": "Updated Description",
            "status": "In Progress",
            "due_date": past_date.strftime("%Y-%m-%d"),
        }

        response = self.client.post(self.update_url, data=invalid_update_data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response.context["form"],
            "due_date",
            "The end date cannot be in the past. Please select today's date or a future date.",
        )
        self.test_task.refresh_from_db()
        self.assertNotEqual(self.test_task.title, invalid_update_data["title"])

    def test_detail_view(self):
        self.client.login(username="testUser", password="Password123")
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["task"], self.test_task)

    def test_task_update_view(self):
        self.client.login(username="testUser", password="Password123")
        future_date = date.today() + timedelta(days=14)
        new_date = {
            "title": "Update test task",
            "description": "description for create update test task",
            "status": "In Progress",
            "due_date": future_date.strftime("%Y-%m-%d"),
        }

        response = self.client.post(self.update_url, data=new_date)
        self.assertEqual(response.status_code, 302)
        self.test_task.refresh_from_db()
        self.assertEqual(self.test_task.title, new_date["title"])

    def test_task_delete_view(self):
        self.assertEqual(Task.objects.count(), 1)
        self.client.login(username="testUser", password="Password123")
        response = self.client.post(self.delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.count(), 0)
