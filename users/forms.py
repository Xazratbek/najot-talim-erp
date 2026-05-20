from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from branches.models import Branch
from .models import User, Roles
import re


class LoginForm(forms.Form):
    login = forms.CharField(
        max_length=15,
        required=True,
        label="Login",
        widget=forms.TextInput(attrs={"placeholder": "Masalan: 41408", "autocomplete": "username"}),
    )
    password = forms.CharField(
        max_length=128,
        required=True,
        label="Parol",
        widget=forms.PasswordInput(attrs={"placeholder": "Parol", "autocomplete": "current-password"}),
    )


class StaffSignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=150, required=True, label="Ism")
    last_name = forms.CharField(max_length=150, required=True, label="Familiya")
    phone = forms.CharField(max_length=20, required=True, label="Telefon")
    branch = forms.ModelChoiceField(
        queryset=Branch.objects.all(),
        required=False,
        label="Filial",
    )

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "phone", "branch", "password1", "password2")

    def clean_username(self):
        username = self.cleaned_data.get("username", "").strip().lower()
        if len(username) != 5:
            raise ValidationError("Login 5 ta belgidan iborat bo'lishi kerak.")
        if User.objects.filter(username=username).exists():
            raise ValidationError("Bu login band.")
        return username

    def clean_phone(self):
        phone = self.cleaned_data.get("phone", "")
        cleaned = re.sub(r"[^\d+]", "", phone)
        if len(cleaned) == 9 and cleaned.isdigit():
            cleaned = f"+998{cleaned}"
        if len(cleaned) == 12 and cleaned.isdigit():
            cleaned = f"+{cleaned}"
        if not re.match(r"^\+998\d{9}$", cleaned):
            raise ValidationError("Telefon formati: +998901234567")
        if User.objects.filter(phone=cleaned).exists():
            raise ValidationError("Bu telefon band.")
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = Roles.ADMIN
        user.is_staff = True
        if commit:
            user.save()
        return user


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "phone",
            "avatar",
            "role",
            "balance",
            "branch",
            "gender",
            "is_active",
        ]


class TeacherCreateForm(UserForm):
    def clean_username(self):
        username = self.cleaned_data.get("username", "").lower()
        if not username:
            raise ValidationError("Username kiritish majburiy")
        if len(username) != 5:
            raise ValidationError("Username 5 ta belgidan iborat bo'lishi kerak")
        if username.isalpha():
            raise ValidationError("Username faqat harfdan iborat bo'lishi mumkin emas")
        if username.isdigit():
            raise ValidationError("Username faqat sondan iborat bo'lishi mumkin emas")
        forbidden = ["admin", "superuser", "root", "moderator", "support"]
        if username in forbidden:
            raise ValidationError("Bu username band qilingan")
        if User.objects.filter(username=username).exists():
            raise ValidationError("Bu username allaqachon band")
        return username


class AdminStudentCreateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "phone", "role", "gender"]
