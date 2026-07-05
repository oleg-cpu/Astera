from datetime import date

from django import forms

from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "due_date", "status"]

        widgets = {"due_date": forms.DateInput(attrs={"type": "date"})}

    def clean_due_date(self):
        due_date = self.cleaned_data.get("due_date")
        if due_date is None:
            return due_date
        elif due_date and due_date < date.today():
            raise forms.ValidationError(
                "The end date cannot be in the past. Please select today's date or a future date."
            )
        return due_date
