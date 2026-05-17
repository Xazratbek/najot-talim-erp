from django.contrib import admin

from .models import Homework, HomeworkSubmission


@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    list_display = ('id', 'group_lesson', 'deadline', 'created_at')
    ordering = ['-id']


@admin.register(HomeworkSubmission)
class HomeworkSubmissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'homework', 'student', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('student__username',)
    ordering = ['-id']
