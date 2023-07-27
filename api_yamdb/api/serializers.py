from datetime import datetime
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from reviews.models import Title, Category, Genre


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
