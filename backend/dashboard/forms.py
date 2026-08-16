from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    phone_number = forms.CharField(
        max_length=15,
        required=False
    )

    city = forms.CharField(
        max_length=100,
        required=False
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "phone_number",
            "city",
            "password1",
            "password2",
        ]


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "form-input",
            "placeholder": "Enter your username",
            "autocomplete": "username",
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-input",
            "placeholder": "Enter your password",
            "autocomplete": "current-password",
        })
    )