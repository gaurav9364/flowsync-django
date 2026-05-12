from django import forms
from .models import Task
from users.models import User


class TaskForm(forms.ModelForm):
    assigned_to = forms.ModelChoiceField(
        queryset=User.objects.filter(role='member'),
        required=True
    )

    class Meta:
        model = Task
        fields = [
            'title',
            'description',
            'project',
            'assigned_to',
            'due_date',
            'status',
            'priority',
        ]