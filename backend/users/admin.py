from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    """Класс для представления модели пользователя в админ-зоне."""
    list_display = ('username', 'email', 'first_name', 'last_name',)
    list_filter = ('username', 'email',)


admin.site.register(User, UserAdmin)
