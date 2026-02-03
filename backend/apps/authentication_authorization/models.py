from django.db import models


class AllowedIPRange(models.Model):
    """
    Modelo para gestionar rangos de IPs permitidas.
    Soporta notación CIDR (ej: 192.168.1.0/24) o IPs individuales.
    """
    network = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Red o IP (CIDR)',
        help_text='Formato CIDR (ej: 192.168.1.0/24) o IP individual (ej: 192.168.1.1)'
    )
    description = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Descripción'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Está activo'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creación'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Fecha de actualización'
    )

    class Meta:
        db_table = 'allowed_ip_range'
        verbose_name = 'Rango IP Permitido'
        verbose_name_plural = 'Rangos IP Permitidos'
        ordering = ['-is_active', 'network']

    def __str__(self):
        return f"{self.network} - {self.description}" if self.description else self.network
