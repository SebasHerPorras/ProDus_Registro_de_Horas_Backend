from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import AllowedIPRange, Role, User


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'code']


class UserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source='role.code', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'full_name', 'username', 'role', 'is_admin', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']


class AllowedIPRangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllowedIPRange
        fields = ['id', 'network', 'description', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['full_name'] = user.full_name
        token['role'] = user.role.code if user.role else None
        token['is_admin'] = user.is_admin
        return token

    def validate(self, attrs):
        username = attrs.get('username')
        if username:
            user = User.objects.filter(username=username).first()
            if user and not user.is_active:
                raise serializers.ValidationError({'detail': 'Usuario inactivo. Contacte al administrador.'})

        data = super().validate(attrs)
        data['ok'] = True
        data['user'] = {
            'id': self.user.id,
            'full_name': self.user.full_name,
            'username': self.user.username,
            'is_active': self.user.is_active,
            'role': self.user.role.code if self.user.role else None,
            'is_admin': self.user.is_admin,
        }
        return data
