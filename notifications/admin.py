from django.contrib import admin

from .forms import NotificationForm
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    form = NotificationForm
    list_display = ('id', 'receiver', 'type', 'title', 'is_read', 'created_at')
    list_filter = ('type', 'is_read', 'created_at')
    search_fields = ('title', 'receiver__username', 'receiver__first_name', 'receiver__last_name')
    autocomplete_fields = ('receiver',)
    readonly_fields = ('created_at', 'updated_at')
