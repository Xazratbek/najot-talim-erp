from django import forms

from .models import Attendance


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['group_lesson', 'student', 'status']
