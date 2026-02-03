"""
URLs del módulo de usuarios.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import UserViewSet, AssistantViewSet, CustomTokenObtainPairView, check_ip

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'assistants', AssistantViewSet, basename='assistant')

urlpatterns = [
    # IP Check (sin autenticación)
    path('auth/check-ip/', check_ip, name='check_ip'),
    
    # JWT Authentication
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # ViewSets
    path('', include(router.urls)),
]
