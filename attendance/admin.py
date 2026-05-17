from django.contrib import admin

from .models import Attendance


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'group_lesson', 'student', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('student__username',)
    ordering = ['-id']
