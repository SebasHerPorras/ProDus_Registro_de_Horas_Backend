from rest_framework import serializers

from apps.projects.models import Project
from apps.users.models import User


class ActiveProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name']


class ActiveCoordinatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'full_name', 'username']