from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm

from .models import User


class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm

    list_display = ('email', 'username', 'fullname', 'is_admin')
    list_filter = ('is_admin',)

    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),

        ('Permissions', {'fields': ('is_admin',)}),
    )

    search_fields = ('email', 'username')
    ordering = ('email', 'username')

    filter_horizontal = ()


admin.site.register(User, UserAdmin)
