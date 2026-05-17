from django.contrib import admin

from .models import Exam, ExamSubmission


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'group', 'started_at', 'ended_at', 'allow_resubmission')
    list_filter = ('allow_resubmission',)
    search_fields = ('title', 'group__name')
    ordering = ['-id']


@admin.register(ExamSubmission)
class ExamSubmissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'exam', 'student', 'checked_by', 'checked_at')
    search_fields = ('student__username', 'exam__title')
    ordering = ['-id']
