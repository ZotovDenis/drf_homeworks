from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_superuser', 'is_staff', 'email', 'role', 'is_active')
    search_fields = ('email', )
    list_filter = ('is_staff', 'is_active', 'role')
