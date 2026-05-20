from django.contrib import admin
from .models import Lesson, LessonRating

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'lesson_date')
    ordering = ['-id']

@admin.register(LessonRating)
class LessonRatingAdmin(admin.ModelAdmin):
    list_display = ('id', 'lesson__title', 'rated_by__username','star')
    ordering = ['-id']
    list_select_related = ['lesson','rated_by']