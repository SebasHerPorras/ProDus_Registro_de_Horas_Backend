from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Serializer personalizado para JWT que incluye datos adicionales del usuario.
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['is_admin'] = user.is_admin
        if hasattr(user, 'person'):
            token['name'] = user.person.name
            token['role'] = user.person.role
        return token
    def validate(self, attrs):
        data = super().validate(attrs)
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
