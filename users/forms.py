from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class SignupForm(UserCreationForm):

    admin_secret_code = forms.CharField(
    required=False,
    widget=forms.PasswordInput(),
    help_text="Required only for admin account creation"
)


    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'phone',
            'role',
            'password1',
            'password2',
        ]

    def clean(self):
        cleaned_data = super().clean()

        role = cleaned_data.get("role")
        code = cleaned_data.get("admin_secret_code")

        if role == "admin":
            if code != "ETHARA_ADMIN_2026":
                raise forms.ValidationError(
                    "Invalid admin secret code."
                )

        return cleaned_data

    

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'phone',
        ]