from django import forms
from .models import Task
from users.models import User
from projects.models import Project


class TaskForm(forms.ModelForm):
    assigned_to = forms.ModelChoiceField(
        queryset=User.objects.filter(role='member'),
        required=True
    )

    project = forms.ModelChoiceField(
        queryset=Project.objects.all(),
        required=True
    )

    widgets = {
        'due_date': forms.DateInput(
            attrs={'type': 'date'}
        ),
    }

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


class SolutionUploadForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            'solution_file',
        ]