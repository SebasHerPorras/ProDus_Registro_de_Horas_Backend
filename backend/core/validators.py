"""
Validadores personalizados para el proyecto.
Incluye validación de IP del instituto usando rangos CIDR.
"""
import ipaddress
from django.core.exceptions import PermissionDenied
from decouple import config


# Modo desarrollo - permitir todas las IPs
DEBUG_ALLOW_ALL_IPS = config('ALLOW_ALL_IPS', default=True, cast=bool)


def get_client_ip(request):
    """
    Obtiene la IP real del cliente considerando proxies.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def validate_institute_ip(request):
    """
    Valida que la petición venga desde la IP del instituto usando rangos CIDR.
    
    Raises:
        PermissionDenied: Si la IP no está en la lista permitida.
    
    Returns:
        str: La IP del cliente si es válida.
    """
    if DEBUG_ALLOW_ALL_IPS:
        return get_client_ip(request)
    
    ip = get_client_ip(request)
    
    if not is_valid_institute_ip(request):
        raise PermissionDenied(
            f"Acceso denegado. Debe conectarse desde la red del instituto. IP detectada: {ip}"
        )
    
    return ip


def is_valid_institute_ip(request):
    """
    Verifica si la IP es válida sin lanzar excepción.
    Consulta el modelo AllowedIPRange para validar contra rangos CIDR.
    
    Returns:
        bool: True si la IP está permitida.
    """
    if DEBUG_ALLOW_ALL_IPS:
        return True
    
    # Import aquí para evitar circular imports
    from apps.authentication_authorization.models import AllowedIPRange
    
    client_ip = get_client_ip(request)
    
    try:
        ip_obj = ipaddress.ip_address(client_ip)
    except ValueError:
        # IP inválida
        return False
    
    # Obtener todos los rangos activos
    allowed_ranges = AllowedIPRange.objects.filter(is_active=True)
    
    for ip_range in allowed_ranges:
        try:
            network = ipaddress.ip_network(ip_range.network, strict=False)
            if ip_obj in network:
                return True
        except ValueError:
            # Formato de red inválido, omitir
            continue
    
    return False
