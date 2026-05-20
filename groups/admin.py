from django.contrib import admin
from .models import *

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'course',
    )
    list_select_related = ['course','branch']
    ordering = ['-id']

@admin.register(GroupTeacher)
class GroupTeacherAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'group',
        'teacher',
    )

    ordering = ['-id']
    list_select_related = ('teacher','group')


@admin.register(GroupStudent)
class GroupStudentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'group',
        'student',
    )
    list_select_related = ('student','group')
    ordering = ['-id']


@admin.register(GroupLesson)
class GroupLessonAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'group',
        'lesson_id',
    )
    list_select_related = ('lesson','group')
    ordering = ['-id']