"""
Serializers para el módulo de usuarios.
"""
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User, Person, Assistant


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Serializer personalizado para JWT que incluye datos adicionales del usuario.
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Agregar claims personalizados al token
        token['username'] = user.username
        token['is_admin'] = user.is_admin
        
        if hasattr(user, 'person'):
            token['name'] = user.person.name
            token['role'] = user.person.role
        
        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Agregar información del usuario a la respuesta
        data['user'] = {
            'id': self.user.id,
            'username': self.user.username,
            'is_admin': self.user.is_admin,
        }
        
        if hasattr(self.user, 'person'):
            data['user']['name'] = self.user.person.name
            data['user']['role'] = self.user.person.role
        
        if hasattr(self.user, 'assistant'):
            data['user']['degree'] = self.user.assistant.degree
            data['user']['is_assistant'] = True
        
        return data


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer básico para User.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'is_admin', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']


class PersonSerializer(serializers.ModelSerializer):
    """
    Serializer para Person.
    """
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Person
        fields = ['user_id', 'username', 'name', 'role', 'is_active']


class AssistantSerializer(serializers.ModelSerializer):
    """
    Serializer para Assistant.
    """
    name = serializers.CharField(source='user.person.name', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    role = serializers.CharField(source='user.person.role', read_only=True)
    
    class Meta:
        model = Assistant
        fields = ['user_id', 'username', 'name', 'role', 'degree', 'hire_date', 'is_active']


class AssistantCreateSerializer(serializers.Serializer):
    """
    Serializer para crear un asistente completo (User + Person + Assistant).
    """
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(write_only=True, min_length=8)
    name = serializers.CharField(max_length=100)
    degree = serializers.CharField(max_length=100)
    hire_date = serializers.DateField()
    
    def create(self, validated_data):
        # Crear User
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        
        # Crear Person
        Person.objects.create(
            user=user,
            name=validated_data['name'],
            role=Person.RoleChoices.ASSISTANT
        )
        
        # Crear Assistant
        assistant = Assistant.objects.create(
            user=user,
            degree=validated_data['degree'],
            hire_date=validated_data['hire_date']
        )
        
        return assistant
