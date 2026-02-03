from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Person, Assistant


class CustomUserCreationForm(UserCreationForm):
    """Formulario para crear usuarios con contraseña hasheada."""
    class Meta:
        model = User
        fields = ('username',)


class CustomUserChangeForm(UserChangeForm):
    """Formulario para editar usuarios."""
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
    
    # Campos para editar usuario existente
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Permisos', {'fields': ('is_admin', 'is_active', 'is_staff', 'is_superuser')}),
    )
    
    # Campos para crear nuevo usuario (con password1 y password2)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'is_admin', 'is_active'),
        }),
    )


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'name', 'role', 'is_active']
    list_filter = ['role', 'is_active']
    search_fields = ['name']


@admin.register(Assistant)
class AssistantAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'get_name', 'degree', 'hire_date', 'is_active']
    list_filter = ['is_active', 'hire_date']
    search_fields = ['degree', 'user__person__name']
    
    def get_name(self, obj):
        return obj.user.person.name if hasattr(obj.user, 'person') else obj.user.username
    get_name.short_description = 'Nombre'


