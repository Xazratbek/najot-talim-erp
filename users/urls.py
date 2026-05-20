from django.urls import path

from .views import LoginView, StaffSignupView

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("staff/signup/", StaffSignupView.as_view(), name="staff-signup"),
]
