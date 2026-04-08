from django.db import models


class AuthorizedIp(models.Model):
    """
    Rangos de IP permitidas para acceso al sistema.
    Luego: soportará CIDR (ej: 10.233.194.0/22)
    """
    ip_address = models.GenericIPAddressField(unique=True, verbose_name='Dirección IP')
    is_active = models.BooleanField(default=True, verbose_name='Activo')

    class Meta:
        db_table = 'authorized_ip'
        verbose_name = 'IP Autorizada'
        verbose_name_plural = 'IPs Autorizadas'

    def __str__(self):
        return str(self.ip_address)


class IpExceptionStatus(models.Model):
    """
    Estados posibles para excepciones de IP (ACTIVE, EXPIRED, REVOKED)
    """
    code = models.CharField(max_length=50, unique=True, verbose_name='Código')

    class Meta:
        db_table = 'ip_exception_status'
        verbose_name = 'Estado de Excepción IP'
        verbose_name_plural = 'Estados de Excepciones IP'
        ordering = ['code']

    def __str__(self):
        return self.code


class IpException(models.Model):
    """
    Excepciones temporales de IP (ej: trabajar desde otro lugar por X días)
    """
    valid_from = models.DateField(verbose_name='Válido desde')
    valid_until = models.DateField(verbose_name='Válido hasta')
    status = models.ForeignKey(
        IpExceptionStatus,
        on_delete=models.PROTECT,
        verbose_name='Estado'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creado')
    created_by = models.ForeignKey(
        'users.User',
        on_delete=models.PROTECT,
        verbose_name='Creado por'
    )

    class Meta:
        db_table = 'ip_exception'
        verbose_name = 'Excepción IP'
        verbose_name_plural = 'Excepciones IP'

    def __str__(self):
        return f"Excepción {self.valid_from} - {self.valid_until}"


class IpExceptionAssistant(models.Model):
    """
    Qué asistentes se benefician de qué excepción
    """
    ip_exception = models.ForeignKey(
        IpException,
        on_delete=models.CASCADE,
        related_name='assistants',
        verbose_name='Excepción'
    )
    assistant = models.ForeignKey(
        'users.Assistant',
        on_delete=models.CASCADE,
        verbose_name='Asistente'
    )

    class Meta:
        db_table = 'ip_exception_assistant'
        verbose_name = 'Asistente en Excepción'
        verbose_name_plural = 'Asistentes en Excepciones'
        unique_together = ('ip_exception', 'assistant')

    def __str__(self):
        return f"{self.assistant} - {self.ip_exception}"