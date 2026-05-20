from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View

from .forms import LoginForm, StaffSignupForm
from .models import Roles


def redirect_after_login(user):
    if user.role == Roles.STUDENT:
        return reverse("student-dashboard")

    if user.role in (Roles.TEACHER, Roles.SUPPORT_TEACHER):
        return "/admin/"

    if user.is_staff or user.is_superuser:
        return "/admin/"
    return reverse("student-dashboard")


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect(redirect_after_login(request.user))
        return render(request, "registration/login.html", {"form": LoginForm()})

    def post(self, request):
        form = LoginForm(request.POST)
        if not form.is_valid():
            return render(request, "registration/login.html", {"form": form})

        user = authenticate(
            request,
            username=form.cleaned_data["login"].strip(),
            password=form.cleaned_data["password"],
        )
        if user is None:
            messages.error(request, "Login yoki parol noto'g'ri.")
            return render(request, "registration/login.html", {"form": form})

        login(request, user)
        return redirect(redirect_after_login(user))


class StaffSignupView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect(redirect_after_login(request.user))
        return render(request, "registration/staff_signup.html", {"form": StaffSignupForm()})

    def post(self, request):
        form = StaffSignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Xodim sifatida ro'yxatdan o'tdingiz. Endi login qiling.")
            return redirect("login")
        return render(request, "registration/staff_signup.html", {"form": form})
