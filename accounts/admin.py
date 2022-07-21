from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm

CustomUser = get_user_model()


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username', 'last_name',]
    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Персональная информация', {
            'fields': ('first_name', 'last_name', 'middle_name', 'email')
        }),
        ('Права доступа', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
            )
        }),
        ('Важные даты', {
            'fields': ('last_login', 'date_joined')
        }),
    )
    add_fieldsets =  ((None, {'fields': (
        'first_name', 'last_name', 'middle_name', 'email',)}),) + UserAdmin.add_fieldsets 


admin.site.register(CustomUser, CustomUserAdmin)
