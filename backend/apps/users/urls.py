from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    AllowedIPRangeViewSet,
    CustomTokenObtainPairView,
    UserViewSet,
    logout_view,
    me_view,
    validate_institute_ip_addr_view,
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'allowed-ip-ranges', AllowedIPRangeViewSet, basename='allowed-ip-range')

urlpatterns = [
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/logout/', logout_view, name='logout'),
    path('auth/me/', me_view, name='auth_me'),
    path('auth/validate-institute-ip/', validate_institute_ip_addr_view, name='validate_institute_ip_addr'),
    path('', include(router.urls)),
]
