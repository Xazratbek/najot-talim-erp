from django.contrib import admin

from .models import Homework, HomeworkSubmission, HomeworkFiles, HomeworkSubmissionFiles

class HomeworkFilesInline(admin.TabularInline):
    model = HomeworkFiles
    extra = 3

class HomeworkSubmissionFilesInline(admin.TabularInline):
    model = HomeworkSubmissionFiles
    extra = 3

class HomeworkSubmissionsInline(admin.TabularInline):
    model = HomeworkSubmission
    extra = 0


@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    inlines = [HomeworkFilesInline,HomeworkSubmissionsInline]
    list_display = ('id', 'group_lesson', 'description','deadline', 'created_at')
    ordering = ['-id']
    list_select_related = ['group_lesson',]


@admin.register(HomeworkSubmission)
class HomeworkSubmissionAdmin(admin.ModelAdmin):
    inlines = [HomeworkSubmissionFilesInline]
    list_display = (
        'id', 'homework', 'student', 'status',
        'checked_by', 'checked_at', 'allow_resubmission', 'created_at',
    )
    list_filter = ('status', 'allow_resubmission')
    search_fields = ('student__username',)
    ordering = ['-id']
    list_select_related = ['homework','student','checked_by']
    list_prefetch_related = ['homeworksubmission_files']
