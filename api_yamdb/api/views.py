from django.contrib.auth import get_user_model
from django.db.models import Avg
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
    CommentSerializer, CategorySerializer, GenreSerializer,
    ReceiveTokenSerializer, ReviewSerializer, SignupSerializer,
    UserSerializer, TitleReadSerializer, TitleWriteSerializer
)
from api.permissions import IsAuthorOrStaff, ReadOnly, IsAdmin
from api.utils import confirm_email_sendler, get_auth_jwt_token
from api.filters import TitleCustomFilter
from reviews.models import Title, Review, Genre, Category


User = get_user_model()


class ListCreateDestroyViewSet(
    ListModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
    GenericViewSet
):
    pass


class GenreViewSet(ListCreateDestroyViewSet):
    """ViewSet модели Genre."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = (ReadOnly | IsAdmin,)


class CategoryViewSet(ListCreateDestroyViewSet):
    """ViewSet модели Category."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = (ReadOnly | IsAdmin,)


class TitleViewSet(ModelViewSet):
    """ViewSet модели Title."""

    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleCustomFilter
    lookup_field = 'id'
    permission_classes = (ReadOnly | IsAdmin,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleReadSerializer
        return TitleWriteSerializer


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
        review = get_object_or_404(
            klass=Review,
            id=self.kwargs.get('review_id'),
            title__id=self.kwargs.get('title_id')
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            klass=Review,
            id=self.kwargs.get('review_id'),
            title__id=self.kwargs.get('title_id')
        )
        serializer.save(author=self.request.user, review=review)


class UserViewSet(ModelViewSet):
    """Работа администратора и superuser с пользователями."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    permission_classes = (IsAdmin,)
    http_method_names = ('get', 'post', 'patch', 'delete', 'head', 'options')

    def perform_update(self, serializer):
        return serializer.save(role=self.request.user.role)

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
        if request.method == 'PATCH':
            return self.partial_update(request, *args, **kwargs)
        return self.retrieve(request, *args, **kwargs)


class SignupView(CreateAPIView):
    """
    Регистрация нового пользователя и отправка кода подтверждения на почту
    указанную пользователем.
    """

    queryset = User.objects.all()
    serializer_class = SignupSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, create = User.objects.get_or_create(**serializer.validated_data)
        confirm_email_sendler(
            email=user.email,
            user=user
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReceiveTokenView(CreateAPIView):
    """Получение JWT-токена для авторизации пользователя.

    Проверка когда подтверждения на валидность. Если код невалидный -
     пользователю возвращается 400й код - bad request.
    """

    queryset = User.objects.all()
    serializer_class = ReceiveTokenSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        """Создание JWT-токена."""
        serializer = ReceiveTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User,
            username=serializer.validated_data.get('username'),
        )
        token = get_auth_jwt_token(user)
        return Response(token, status=status.HTTP_200_OK)
