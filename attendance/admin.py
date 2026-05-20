from django.contrib import admin

from .models import Attendance


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'group_lesson', 'student', 'status', 'created_at')
    list_filter = ('status',)
    autocomplete_fields = ['student']
    search_fields = ('student__username',)
    ordering = ['-id']
    list_select_related = ['group_lesson','student']
