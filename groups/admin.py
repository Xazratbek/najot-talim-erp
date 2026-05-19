from django.contrib import admin

from .models import (
    Group,
    GroupTeacher,
    GroupStudent,
    GroupLesson,
)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'course',
    )

    ordering = ['-id']


@admin.register(GroupTeacher)
class GroupTeacherAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'group',
        'teacher',
    )

    ordering = ['-id']


@admin.register(GroupStudent)
class GroupStudentAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'group',
        'student',
    )
    list_select_related = ('group', 'student')

    ordering = ['-id']


@admin.register(GroupLesson)
class GroupLessonAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'group',
        'lesson_id',
    )

    ordering = ['-id']