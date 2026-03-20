from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import AllowedIPRange, Role, User, Assistant


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
    
class AssistantCreateSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    full_name = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)
    is_active = serializers.BooleanField(required=False, default=True)

    start_date = serializers.DateField()
    end_date = serializers.DateField(required=False, allow_null=True)
    weekly_hours = serializers.IntegerField(min_value=1, max_value=168)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('Ya existe un usuario con ese username.')
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({'password_confirm': 'Las contraseñas no coinciden.'})
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('password_confirm', None)

        role, _ = Role.objects.get_or_create(code='assistant')

        user = User.objects.create_user(
            username=validated_data['username'],
            password=password,
            full_name=validated_data['full_name'],
            is_active=validated_data.get('is_active', True),
            is_admin=False,
        )
        user.role = role
        user.save(update_fields=['role'])

        assistant = Assistant.objects.create(
            user=user,
            start_date=validated_data['start_date'],
            end_date=validated_data.get('end_date'),
            weekly_hours=validated_data['weekly_hours'],
        )

        return {
            'user': UserSerializer(user).data,
            'assistant': {
                'user_id': user.id,
                'start_date': assistant.start_date,
                'end_date': assistant.end_date,
                'weekly_hours': assistant.weekly_hours,
            }
        }
    
class AssistantListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='user.id', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    full_name = serializers.CharField(source='user.full_name', read_only=True)
    is_active = serializers.BooleanField(source='user.is_active', read_only=True)

    class Meta:
        model = Assistant
        fields = ['id', 'username', 'full_name', 'is_active']