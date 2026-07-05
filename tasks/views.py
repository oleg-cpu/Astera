from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from tasks.models import Task

from .forms import TaskForm


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "tasks/task_list.html"
    context_object_name = "tasks"

    def get_queryset(self):
        return self.model.objects.filter(user_id=self.request.user).order_by("creation_date")


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

    def get_queryset(self):
        return super().get_queryset().filter(user_id=self.request.user)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_update_form.html"
    success_url = reverse_lazy("task-list")

    def get_queryset(self):
        return super().get_queryset().filter(user_id=self.request.user)


class TaskDeleteView(LoginRequiredMixin, DeleteView): # type: ignore[misc]
    model = Task
    template_name = "tasks/task_delete.html"
    success_url = reverse_lazy("task-list")

    def get_queryset(self):
        return super().get_queryset().filter(user_id=self.request.user)
