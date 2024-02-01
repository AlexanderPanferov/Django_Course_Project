from django.contrib import admin

from users.models import User


class CustomUserAdmin(admin.ModelAdmin):
    """Класс для блокировки пользователя"""
    list_display = ('email', 'is_blocked')
    actions = ['block_users', 'unblock_users']

    def block_users(self, request, queryset):
        queryset.update(is_blocked=True)

    def unblock_users(self, request, queryset):
        queryset.update(is_blocked=False)


admin.site.register(User, CustomUserAdmin)
