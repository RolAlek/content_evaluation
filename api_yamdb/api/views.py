from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import viewsets, permissions, status
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from rest_framework.mixins import (
    ListModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
)
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.generics import CreateAPIView
from django_filters.rest_framework import DjangoFilterBackend

from api.serializers import (
    CommentSerializer, ReviewSerializer, UserSerializer,
    TitleSerializer, CategorySerializer, GenreSerializer
)
    CommentSerializer, CategorySerializer, GenreSerializer,
    ReceiveTokenSerializer, ReviewSerializer, SignupSerializer,
    TitleSerializer, UserSerializer
)
from api.pagination import TitleCategoryGenrePagination
from api.permissions import IsAuthorOrStaff, ReadOnly, IsAdmin
from api.utils import confirm_email_sendler, get_auth_jwt_token
from reviews.models import Title, Review, Genre, Category

User = get_user_model()


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
    lookup_field = 'slug'
    permission_classes = (ReadOnly | IsAdmin,)


class CategoryViewSet(ListСreateDestroyViewSet):
    """ViewSet модели Category."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = (ReadOnly | IsAdmin,)


class TitleViewSet(ModelViewSet):
    """ViewSet модели Title."""

    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'year', 'category__slug', 'genre__slug')
    lookup_field = 'id'
    permission_classes = (ReadOnly | IsAdmin,)

    def perform_create(self, serializer):
        serializer.save(
            # Не использую get_object_or_404,
            # т.к. в TitleSerializer в полеgenre не выставляется many=True
            genre=Genre.objects.all().filter(slug=self.request.data['genre']),
            category=get_object_or_404(
                Category, slug=self.request.data['category'])
        )

    def perform_update(self, serializer):
        if ('genre' in self.request.data
           and 'category' in self.request.data):
            serializer.save(
                genre=Genre.objects.all().
                filter(slug=self.request.data['genre']),
                category=get_object_or_404(
                    Category, slug=self.request.data['category'])
            )
        elif 'category' in self.request.data:
            serializer.save(
                category=get_object_or_404(
                    Category, slug=self.request.data['category'])
            )
        elif 'genre' in self.request.data:
            serializer.save(
                genre=Genre.objects.all().
                filter(slug=self.request.data['genre']),
            )
        serializer.save()


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет отзывов."""

    serializer_class = ReviewSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrStaff,
    )

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет комментариев."""

    serializer_class = CommentSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrStaff,
    )

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


class UserViewSet(ModelViewSet):
    """Вьюсет обрабатывающий запросы к эндпоинту 'users'."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    permission_classes = (IsAdmin,)

    def get_instance(self):
        return self.request.user

    @action(
        methods=['get', 'patch'],
        detail=False,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def me(self, request, *args, **kwargs):
        """
        Маршрутизация дополнительных действий при GET-, PATCH-запросах к
         api/v1/users/me/.

        При GET-запросе к эндпоинту получение данных своей учетной записи.
        При PATCH-запросе изменение данных своей учетной записи.
        """

        self.get_object = self.get_instance
        if request.method == "GET":
            return self.retrieve(request, *args, **kwargs)
        elif request.method == "PATCH":
            return self.partial_update(request, *args, **kwargs)


class SignupView(CreateAPIView):
    """Регистрации нового пользователя и подтверждение по почте."""

    queryset = User.objects.all()
    serializer_class = SignupSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.create(**serializer.validated_data)
        confirm_code = default_token_generator.make_token(user)
        confirm_email_sendler(
            email=user.email,
            confirm_code=confirm_code
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReceiveTokenView(CreateAPIView):
    """Получение JWT-токена для авторизации пользователя."""
    queryset = User.objects.all()
    serializer_class = ReceiveTokenSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = ReceiveTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = get_object_or_404(
            User,
            username=serializer.validated_data.get('username'),
        )
        token = get_auth_jwt_token(user)
        return Response(token, status=status.HTTP_200_OK)
