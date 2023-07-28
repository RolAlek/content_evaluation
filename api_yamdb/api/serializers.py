from datetime import datetime
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
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


class TitleSerializer(serializers.ModelSerializer):
    """Serializer модели Title."""

    rating = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=None
    )
    genre = SlugRelatedField(
        slug_field='slug',
        read_only=True
    )
    category = SlugRelatedField(
        slug_field='slug',
        read_only=True
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description',
                  'genre', 'category'
                  )

    def validate(self, data):
        if data['year'] > datetime.now().year:
            raise ValueError('Произведение не может быть из будущего')
        return data


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
        read_only_fields = ('title', 'author')


class CommentSerializer(serializers.ModelSerializer):
    """Сериализация комментариев."""

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
        read_only_fields = ('review', 'author')

