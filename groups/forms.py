from django import forms

from .models import Group, GroupLesson, GroupStudent, GroupTeacher


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'course', 'branch', 'started_at', 'ended_at', 'is_opened']


class GroupTeacherForm(forms.ModelForm):
    class Meta:
        model = GroupTeacher
        fields = ['group', 'teacher']


class GroupStudentForm(forms.ModelForm):
    class Meta:
        model = GroupStudent
        fields = ['group', 'student', 'joined_at']


class GroupLessonForm(forms.ModelForm):
    class Meta:
        model = GroupLesson
        fields = ['group', 'lesson']
