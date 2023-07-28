from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для CustomUser модели."""

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        lookup_field = 'username'


class SignupSerializer(serializers.ModelSerializer):
    """Сериализатор регистрации нового пользователя."""

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate(self, attrs):
        username = attrs.get('username')

        if username.lower() == 'me':
            raise serializers.ValidationError(
                'Использовать "me" в качестве имени пользователя запрещено!'
            )
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                f'Пользователь с именем {username} существует!'
                f' Придумайте другое имя!'
            )
        if User.objects.filter(email=attrs.get('email')).exists():
            raise serializers.ValidationError(
                'Пользователь с таким email уже существует!'
            )
        return attrs

# TODO: доделать авторизацию по токену
class ReceiveTokenSerializer(serializers.ModelSerializer):
    ...
