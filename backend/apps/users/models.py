"""
Modelos de usuarios según el diagrama ER:
- User: Usuario base con autenticación
- Person: Información personal del usuario
- Assistant: Datos específicos de asistentes
"""
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    """
    Manager personalizado para el modelo User.
    """
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
    """
    Modelo User personalizado.
    Campos según diagrama: UserId, UserName, PasswordHash, IsAdmin, IsActive
    """
    username = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Nombre de usuario'
    )
    is_admin = models.BooleanField(
        default=False,
        verbose_name='Es administrador'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Está activo'
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name='Es staff'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creación'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Fecha de actualización'
    )
    
    objects = UserManager()
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    
    class Meta:
        db_table = 'user'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
    
    def __str__(self):
        return self.username


class Person(models.Model):
    """
    Modelo Person - Información personal del usuario.
    Campos según diagrama: UserId (FK), Name, Role, IsActive
    """
    class RoleChoices(models.TextChoices):
        ASSISTANT = 'ASSISTANT', 'Asistente'
        PROJECT_COORDINATOR = 'PROJECT_COORDINATOR', 'Coordinador de Proyecto'
        GENERAL_COORDINATOR = 'GENERAL_COORDINATOR', 'Coordinador General'
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='person',
        verbose_name='Usuario'
    )
    name = models.CharField(
        max_length=100,
        verbose_name='Nombre completo'
    )
    role = models.CharField(
        max_length=50,
        choices=RoleChoices.choices,
        default=RoleChoices.ASSISTANT,
        verbose_name='Rol'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Está activo'
    )
    
    class Meta:
        db_table = 'person'
        verbose_name = 'Persona'
        verbose_name_plural = 'Personas'
    
    def __str__(self):
        return f"{self.name} ({self.get_role_display()})"


class Assistant(models.Model):
    """
    Modelo Assistant - Datos específicos de asistentes.
    Campos según diagrama: UserId (FK), Degree, HireDate, IsActive
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='assistant',
        verbose_name='Usuario'
    )
    degree = models.CharField(
        max_length=100,
        verbose_name='Carrera/Grado'
    )
    hire_date = models.DateField(
        verbose_name='Fecha de contratación'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Está activo'
    )
    
    class Meta:
        db_table = 'assistant'
        verbose_name = 'Asistente'
        verbose_name_plural = 'Asistentes'
    
    def __str__(self):
        if hasattr(self.user, 'person'):
            return f"{self.user.person.name} - {self.degree}"
        return f"{self.user.username} - {self.degree}"


