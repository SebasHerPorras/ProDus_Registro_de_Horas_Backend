"""
URLs del módulo de usuarios.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, AssistantViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'assistants', AssistantViewSet, basename='assistant')

urlpatterns = [
    # ViewSets
    path('', include(router.urls)),
]
