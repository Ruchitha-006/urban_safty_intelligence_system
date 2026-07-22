from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm


def landing_view(request):
    return render(request, "authentication/index.html")


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    form = LoginForm(request, data=request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            login(request, form.get_user())
            return redirect("dashboard")

    return render(request, "authentication/login.html", {"form": form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    form = RegisterForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")

    return render(request, "authentication/register.html", {"form": form})


@login_required
def logout_view(request):
    logout(request)
    return redirect("landing")