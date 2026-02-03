"""
Configuración de paginación para el proyecto.
"""
from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    """
    Paginación estándar para listados.
    """
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class LargeResultsSetPagination(PageNumberPagination):
    """
    Paginación para listados grandes.
    """
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 200
