from datetime import datetime

from django.contrib.auth.tokens import default_token_generator
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.models import Comment, Category, Genre, Title, Review

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    """Serializer модели Categories."""

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Serializer модели Genres."""

    class Meta:
        model = Genre
        fields = ('name', 'slug')
        lookup_field = 'slug'


class TitleReadSerializer(serializers.ModelSerializer):
    """Serializer модели Title."""

    rating = serializers.IntegerField(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description',
                  'genre', 'category'
                  )


class TitleWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True,
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description',
                  'genre', 'category'
                  )

    def validate(self, data):
        if (
            'year' in data
            and data['year'] > int(datetime.now().year)
        ):
            raise ValueError('Произведение не может быть из будущего')
        return data


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализация отзывов."""

    author = serializers.StringRelatedField(
        read_only=True,
    )

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context.get('view').kwargs.get('title_id')

        if (
            request.method == 'POST'
            and author.reviews.filter(title_id=title_id).exists()
        ):
            raise serializers.ValidationError(
                'Можно оставить только один отзыв для произведения!'
            )
        return data

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    """Сериализация комментариев."""

    author = serializers.StringRelatedField(
        read_only=True,
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
        read_only_fields = ('review', 'author')


class UserSerializer(serializers.ModelSerializer):
    """Сериализация работы с пользователями."""

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        lookup_field = 'username'


class SignupSerializer(serializers.ModelSerializer):
    """Сериализация регистрации нового пользователя."""

    username = serializers.CharField(
        max_length=150,
        required=True,
        validators=(
            RegexValidator(
                regex=r'^[\w.@+-]+$',
                message='Имя пользователя содержит недопустимые символы'
            ),
        ),
    )
    email = serializers.EmailField(max_length=254, required=True)

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate(self, attrs):
        """
        Запрет на использование 'me' в качестве имени пользователя.
        Проверки на использование неуникального email и username.
        """
        email = attrs.get('email')
        username = attrs.get('username')
        user_to_username = User.objects.filter(username=username).exists()
        user_to_email = User.objects.filter(email=email).exists()

        if username.lower() == 'me':
            raise serializers.ValidationError(
                'Использовать "me" в качестве имени пользователя запрещено!'
            )
        if user_to_email and not user_to_username:
            raise serializers.ValidationError(
                f'Пользователь с email {email} уже существует!'
            )
        if user_to_username and not user_to_email:
            raise serializers.ValidationError(
                f'Имя пользователя "{username}" уже занято!'
            )
        return attrs


class ReceiveTokenSerializer(serializers.Serializer):
    """Сериализация получения jwt-токена."""

    username = serializers.CharField(max_length=150, required=True)
    confirmation_code = serializers.CharField(max_length=150, required=True)

    def validate(self, attrs):
        user = get_object_or_404(User, username=attrs.get('username'))
        confirmation_code = attrs.get('confirmation_code')
        if not default_token_generator.check_token(user, confirmation_code):
            raise serializers.ValidationError('Неверный код подтверждения!')
        return attrs
