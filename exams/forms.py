from django import forms

from .models import Exam, ExamSubmission


class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['group', 'title', 'description', 'started_at', 'ended_at', 'allow_resubmission']


class ExamSubmissionForm(forms.ModelForm):
    class Meta:
        model = ExamSubmission
        fields = ['exam', 'student', 'file', 'description']
