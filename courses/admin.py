from django.contrib import admin

from .models import Course, CourseCategory

@admin.register(CourseCategory)
class CourseCategoryAdmin(admin.ModelAdmin):
    list = ['id','title','created_at']

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'title',
        'category'
    )

    ordering = ['-id']