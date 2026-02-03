"""
Excepciones personalizadas para el proyecto.
"""
from rest_framework.exceptions import APIException
from rest_framework import status


class IPNotAllowedException(APIException):
    """
    Excepción cuando la IP no está permitida.
    """
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "Acceso denegado. Debe conectarse desde la red del instituto."
    default_code = "ip_not_allowed"


class InvalidCredentialsException(APIException):
    """
    Excepción para credenciales inválidas.
    """
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "Credenciales inválidas."
    default_code = "invalid_credentials"


class UserInactiveException(APIException):
    """
    Excepción cuando el usuario está inactivo.
    """
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "Usuario inactivo. Contacte al administrador."
    default_code = "user_inactive"


class ReportAlreadyApprovedException(APIException):
    """
    Excepción cuando se intenta modificar un reporte ya aprobado.
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "No se puede modificar un reporte ya aprobado."
    default_code = "report_already_approved"


class InvalidTimeRangeException(APIException):
    """
    Excepción para rangos de tiempo inválidos.
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "El rango de tiempo es inválido."
    default_code = "invalid_time_range"
