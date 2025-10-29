from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from tasks.models import Task
from .forms import TaskForm

class TaskListView(ListView):
    model = Task
    template_name = "tasks/task_list.html"


class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("task-list")
