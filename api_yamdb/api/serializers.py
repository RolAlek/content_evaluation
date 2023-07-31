from datetime import datetime
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from reviews.models import Title, Review, Comment, Category, Genre


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для CustomUser модели."""

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        lookup_field = 'username'


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


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализация отзывов."""

    author = serializers.StringRelatedField(
        read_only=True,
    )

    def validate_score(self, value):
        if 0 > value > 10:
            raise serializers.ValidationError('Оценка может быть от 1 до 10!')
        return value

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if (
            request.method == 'POST'
            and Review.objects.filter(title=title, author=author).exists()
        ):
            raise serializers.ValidationError(
                'Можно оставить только один отзыв для произведения!'
            )
        return data

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review


class TitleSerializer(serializers.ModelSerializer):
    """Serializer модели Title."""
    rating = serializers.IntegerField(read_only=True,)
    genre = GenreSerializer(read_only=False, many=True, required=False)
    category = CategorySerializer(read_only=False, required=False)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description',
                  'genre', 'category'
                  )

    def validate(self, data):
        print(data)
        if ('year' in data
           and data['year'] > int(datetime.now().year)):
            raise ValueError('Произведение не может быть из будущего')
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализация комментариев."""

    author = serializers.StringRelatedField(
        read_only=True,
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
        read_only_fields = ('review', 'author')


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


class ReceiveTokenSerializer(serializers.Serializer):
    """Сериализация получения jwt-токена."""

    username = serializers.CharField(max_length=150, required=True)
    confirm_code = serializers.CharField(max_length=150, required=True)