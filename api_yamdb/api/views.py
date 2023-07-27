from rest_framework.mixins import (
    ListModelMixin, CreateModelMixin, DestroyModelMixin)
from rest_framework.viewsets import (
    ModelViewSet, GenericViewSet)
from rest_framework.filters import SearchFilter

from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

from reviews.models import Genre, Category, Title
from api.serializers import (
    TitleSerializer,
    CategorySerializer,
    GenreSerializer
)
from api.pagination import TitleCategoryGenrePagination


class ListСreateDestroyViewSet(
    ListModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
    GenericViewSet
):
    pass


class GenreViewSet(ListСreateDestroyViewSet):
    """ViewSet модели Genre."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ('name',)
    pagination_class = TitleCategoryGenrePagination
    lookup_field = 'slug'
    # необходимо добваить permissions


class CategoryViewSet(ListСreateDestroyViewSet):
    """ViewSet модели Category."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ('name',)
    pagination_class = TitleCategoryGenrePagination
    lookup_field = 'slug'
    # необходимо добваить permissions


class TitleViewSet(ModelViewSet):
    """ViewSet модели Title."""
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'year', 'category__slug', 'genre__slug')
    pagination_class = TitleCategoryGenrePagination
    lookup_field = 'id'
    # необходимо добваить permissions

    def perform_create(self, serializer):
        serializer.save(
            genre=get_object_or_404(Genre, slug=self.request.POST['genre']),
            category=get_object_or_404(
                Category, slug=self.request.POST['category'])
        )
