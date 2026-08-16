from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm, LoginForm


# ============================================================
# LANDING PAGE
# ============================================================

def landing_view(request):
    """
    Main Urban Vigilance landing page.
    """

    return render(
        request,
        "authentication/index.html"
    )


# ============================================================
# LOGIN
# ============================================================

def login_view(request):
    """
    Handles user login.
    """

    # Already logged in
    if request.user.is_authenticated:
        return redirect("dashboard")

    form = LoginForm(
        request,
        data=request.POST or None
    )

    if request.method == "POST":

        if form.is_valid():

            user = form.get_user()

            login(
                request,
                user
            )

            return redirect("dashboard")

    return render(
        request,
        "authentication/login.html",
        {
            "form": form
        }
    )


# ============================================================
# REGISTER
# ============================================================

def register_view(request):
    """
    Handles new user registration.
    """

    # Already logged in
    if request.user.is_authenticated:
        return redirect("dashboard")

    form = RegisterForm(
        request.POST or None
    )

    if request.method == "POST":

        if form.is_valid():

            user = form.save()

            login(
                request,
                user
            )

            return redirect("dashboard")

    return render(
        request,
        "authentication/register.html",
        {
            "form": form
        }
    )


# ============================================================
# LOGOUT
# ============================================================

@login_required
def logout_view(request):
    """
    Logs the current user out.
    """

    logout(request)

    return redirect("landing")