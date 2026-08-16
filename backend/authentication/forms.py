from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm
)
from django.contrib.auth.models import User


# ============================================================
# LOGIN FORM
# ============================================================

class LoginForm(AuthenticationForm):

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-input",
                "placeholder": "Username",
                "autocomplete": "username",
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-input",
                "placeholder": "Password",
                "autocomplete": "current-password",
            }
        )
    )


# ============================================================
# REGISTER FORM
# ============================================================

class RegisterForm(UserCreationForm):

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class": "form-input",
                "placeholder": "Email",
                "autocomplete": "email",
            }
        )
    )

    class Meta:

        model = User

        fields = (
            "username",
            "email",
            "password1",
            "password2",
        )

        widgets = {

            "username": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "Username",
                    "autocomplete": "username",
                }
            ),

        }