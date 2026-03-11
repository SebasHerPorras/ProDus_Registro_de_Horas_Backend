"""
URLs para autenticación y autorización.
"""
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import CustomTokenObtainPairView, validate_institute_ip_addr_view, logout_view


urlpatterns = [
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/logout/', logout_view, name='logout'),
    path('auth/validate-institute-ip/', validate_institute_ip_addr_view, name='validate_institute_ip_addr'),
]
