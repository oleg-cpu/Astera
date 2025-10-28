import uuid
from django.db import models


class Task(models.Model):
    STATUS_CHOICES = (
        ("To Do", "To Do"),
        ("In Progress", "In Progress"),
        ("Done", "Done")
    )

    id_task = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=50, blank=False, null=False)
    description = models.CharField(max_length=500, blank=False)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default="To Do")
    creation_date = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    due_date = models.DateField(blank=False, null=False)
    user_id = models.ForeignKey('users.User', editable=False, null=True, on_delete=models.CASCADE)

