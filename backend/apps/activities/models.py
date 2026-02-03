"""
Modelos de actividades según el diagrama ER:
- Activity: Catálogo de actividades disponibles
"""
from django.db import models


class Activity(models.Model):
    """
    Modelo Activity - Catálogo de actividades.
    Campos según diagrama: ActivityId, Name, Category, IsActive
    """
    name = models.CharField(
        max_length=100,
        verbose_name='Nombre de la actividad'
    )
    category = models.CharField(
        max_length=50,
        verbose_name='Categoría'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Está activa'
    )
    
    class Meta:
        db_table = 'activity'
        verbose_name = 'Actividad'
        verbose_name_plural = 'Actividades'
        ordering = ['category', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.category})"
