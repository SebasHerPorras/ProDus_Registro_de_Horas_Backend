from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import AllowedIPRange, User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    list_display = ['id', 'username', 'is_admin', 'is_active', 'created_at']
    list_filter = ['is_admin', 'is_active']
    search_fields = ['username']
    ordering = ['username']

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Permisos', {'fields': ('is_admin', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'is_admin', 'is_active'),
        }),
    )


@admin.register(AllowedIPRange)
class AllowedIPRangeAdmin(admin.ModelAdmin):
    list_display = ['network', 'description', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['network', 'description']
    ordering = ['-is_active', 'network']
