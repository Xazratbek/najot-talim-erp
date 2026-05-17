from django import forms

from .models import Homework, HomeworkSubmission


class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        fields = ['group_lesson', 'file', 'description', 'deadline']


class HomeworkSubmissionForm(forms.ModelForm):
    class Meta:
        model = HomeworkSubmission
        fields = ['homework', 'student', 'file', 'description', 'status']
