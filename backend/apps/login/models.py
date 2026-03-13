from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('El usuario debe tener un nombre de usuario')

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True, verbose_name='Nombre de usuario')
    is_admin = models.BooleanField(default=False, verbose_name='Es administrador')
    is_active = models.BooleanField(default=True, verbose_name='Está activo')
    is_staff = models.BooleanField(default=False, verbose_name='Es staff')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'user'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return self.username


class AllowedIPRange(models.Model):
    network = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Red o IP (CIDR)',
        help_text='Formato CIDR (ej: 192.168.1.0/24) o IP individual (ej: 192.168.1.1)',
    )
    description = models.CharField(max_length=200, blank=True, verbose_name='Descripción')
    is_active = models.BooleanField(default=True, verbose_name='Está activo')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')

    class Meta:
        db_table = 'allowed_ip_range'
        verbose_name = 'Rango IP Permitido'
        verbose_name_plural = 'Rangos IP Permitidos'
        ordering = ['-is_active', 'network']

    def __str__(self):
        return f"{self.network} - {self.description}" if self.description else self.network
