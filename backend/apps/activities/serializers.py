"""
Serializers para el módulo de actividades.
"""
from rest_framework import serializers
from .models import Activity


class ActivitySerializer(serializers.ModelSerializer):
    """
    Serializer para Activity.
    """
    class Meta:
        model = Activity
        fields = ['id', 'name', 'category', 'is_active']
        read_only_fields = ['id']
