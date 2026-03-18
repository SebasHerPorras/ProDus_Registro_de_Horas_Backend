from .validators import get_client_ip, is_valid_institute_ip


def validate_institute_ip_addr(request):
    client_ip = get_client_ip(request)
    is_allowed = is_valid_institute_ip(request)

    return {
        'allowed': is_allowed,
        'client_ip': client_ip,
        'message': 'Acceso permitido' if is_allowed else 'Acceso denegado - IP no autorizada',
    }
