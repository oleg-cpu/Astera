from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from datetime import date, timedelta

from tasks.models import Task


class TaskViewTest(TestCase):
    def setUp(self):
        User_model = get_user_model()
        self.user = User_model.objects.create_user(username='testUser', password='Password123')

        self.list_url = reverse('task-list')
        self.create_url = reverse("create-task")

        self.test_task = Task.objects.create(
            title = "test task",
            description = "Description for test task",
            status = "To Do",
            due_date = date.today() + timedelta(days=7),
            user_id = self.user
        )

    def test_task_list_view_authenticated(self):
        loged_in = self.client.login(username="testUser", password="Password123")
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
        loged_in = self.client.login(username="testUser", password="Password123")
        future_date = date.today() + timedelta(days=7)
        form_data = {
            "title": "create test task",
            "description" : "description for create test task",
            "status": "To Do",
            "due_date": future_date.strftime('%Y-%m-%d'),
            }
        response = self.client.post(self.create_url, data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.list_url)
        self.assertEqual(Task.objects.count(), 2)
        new_task = Task.objects.get(title="create test task")
        self.assertEqual(new_task.user_id, self.user)
