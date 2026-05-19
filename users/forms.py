from django import forms

from .models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'phone',
            'avatar',
            'role',
            'balance',
            'branch',
            'gender',
            'is_active',
        ]


class AdminStudentCreateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'phone',
            'role',
            'gender'
        ]
