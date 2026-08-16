from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email address",
                "autocomplete": "email",
            }
        )
    )

    phone_number = forms.CharField(
        required=False,
        max_length=15,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Phone number",
                "autocomplete": "tel",
            }
        )
    )

    city = forms.CharField(
        required=False,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "placeholder": "City",
                "autocomplete": "address-level2",
            }
        )
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

    def save(self, commit=True):
        user = super().save(commit=False)

        user.email = self.cleaned_data["email"]

        if commit:
            user.save()

        return user


class LoginForm(forms.Form):

    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "autocomplete": "username",
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "autocomplete": "current-password",
            }
        )
    )

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.request = request
        self.user_cache = None

    def clean(self):
        cleaned_data = super().clean()

        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password:

            self.user_cache = authenticate(
                self.request,
                username=username,
                password=password,
            )

            if self.user_cache is None:
                raise forms.ValidationError(
                    "Invalid username or password."
                )

            if not self.user_cache.is_active:
                raise forms.ValidationError(
                    "This account is inactive."
                )

        return cleaned_data

    def get_user(self):
        return self.user_cache