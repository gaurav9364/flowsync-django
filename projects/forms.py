from django.contrib.auth.decorators import login_required
from django import forms
from .models import Project
from users.models import User
from .models import Team



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
        widgets = {
            'start_date': forms.DateInput(
                attrs={'type': 'date'}
            ),
            'end_date': forms.DateInput(
                attrs={'type': 'date'}
            ),
        }

class TeamForm(forms.ModelForm):
    members = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(role='member'),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Team
        fields = [
            'name',
            'description',
            'members',
        ]