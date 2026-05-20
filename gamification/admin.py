from django.contrib import admin
from .models import XP,Rating

@admin.register(XP)
class XPAdmin(admin.ModelAdmin):
    list_display = ['student__username','amount','kumushlar','reason']
    list_select_related = ['student']

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['student__username','level']
    list_select_related = ['student']
