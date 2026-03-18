import ipaddress

from decouple import config
from django.core.exceptions import PermissionDenied


DEBUG_ALLOW_ALL_IPS = config('ALLOW_ALL_IPS', default=False, cast=bool)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


def validate_institute_ip(request):
    if DEBUG_ALLOW_ALL_IPS:
        return get_client_ip(request)

    ip = get_client_ip(request)
    if not is_valid_institute_ip(request):
        raise PermissionDenied(
            f'Acceso denegado. Debe conectarse desde la red del instituto. IP detectada: {ip}'
        )
    return ip


def is_valid_institute_ip(request):
    if DEBUG_ALLOW_ALL_IPS:
        return True

    from .models import AllowedIPRange

    client_ip = get_client_ip(request)

    try:
        ip_obj = ipaddress.ip_address(client_ip)
    except ValueError:
        return False

    allowed_ranges = AllowedIPRange.objects.filter(is_active=True)
    for ip_range in allowed_ranges:
        try:
            network = ipaddress.ip_network(ip_range.network, strict=False)
            if ip_obj in network:
                return True
        except ValueError:
            continue

    return False


def is_valid_institute_ip_specific(ip_address):
    if DEBUG_ALLOW_ALL_IPS:
        return True

    from .models import AllowedIPRange

    try:
        ip_obj = ipaddress.ip_address(ip_address)
    except ValueError:
        return False

    allowed_ranges = AllowedIPRange.objects.filter(is_active=True)
    for ip_range in allowed_ranges:
        try:
            network = ipaddress.ip_network(ip_range.network, strict=False)
            if ip_obj in network:
                return True
        except ValueError:
            continue

    return False
