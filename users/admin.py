from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        'id',
        'username',
        'first_name',
        'last_name',
        'role',
    )
    ordering = ['-id']
    fieldsets = UserAdmin.fieldsets + (
        (
            "Qo'shimcha ma'lumotlar",
            {
                'fields': (
                    'phone',
                    'avatar',
                    'role',
                    'balance',
                    'branch',
                    'gender',
                )
            }
        ),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Qo'shimcha ma'lumotlar",
            {
                'classes': ('wide',),
                'fields': (
                    'first_name',
                    'last_name',
                    'phone',
                    'role',
                    'branch',
                    'gender',
                ),
            },
        ),
    )
    list_select_related = ['branch']