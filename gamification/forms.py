from django import forms

from .models import XP


class XPForm(forms.ModelForm):
    class Meta:
        model = XP
        fields = ['student', 'amount', 'reason']
