from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.generics import CreateAPIView
from rest_framework.filters import SearchFilter
from rest_framework import status

from .serializers import (
    ReceiveTokenSerializer, SignupSerializer, User, UserSerializer
)
from .utils import confirm_email_sendler, get_auth_jwt_token


class UserViewSet(ModelViewSet):
    """Вьюсет обрабатывающий запросы к эндпоинту 'users'."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    def get_instance(self):
        return self.request.user

    @action(methods=['get', 'patch'], detail=False)
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
    permission_classes = (AllowAny,)

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
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = ReceiveTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = get_object_or_404(
            User,
            username=serializer.validated_data.get('username'),
        )
        token = get_auth_jwt_token(user)
        return Response(token, status=status.HTTP_200_OK)
