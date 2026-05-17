from django import forms

from .models import Notification


class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = [
            'receiver',
            'type',
            'title',
            'is_read',
        ]
