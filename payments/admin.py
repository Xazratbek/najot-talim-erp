from django.contrib import admin

from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'amount', 'payment_type', 'paid_at')
    list_filter = ('payment_type',)
    search_fields = ('student__username', 'student__phone')
    ordering = ['-id']
