from django import forms

from .models import Course, CourseCategory


class CourseCategoryForm(forms.ModelForm):
    class Meta:
        model = CourseCategory
        fields = ['title']


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['category', 'title', 'price']
