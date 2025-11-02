from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from tasks.models import Task
from .forms import TaskForm

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "tasks/task_list.html"
    

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("task-list")

    def form_valid(self, form):
        form.instance.user_id = self.request.user
        return super().form_valid(form)


class TaskDetailView(LoginRequiredMixin, DetailView):

    model = Task
    template_name = "tasks/task_detail.html"


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_update_form.html"
    success_url = reverse_lazy("task-list")


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = "tasks/task_delete.html"
    success_url = reverse_lazy("task-list")
