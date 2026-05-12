from django.contrib.auth.decorators import login_required
from django import forms
from .models import Project
from users.models import User


class ProjectForm(forms.ModelForm):
    members = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(role='member'),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Project
        fields = [
            'name',
            'description',
            'members',
            'start_date',
            'end_date',
        ]