from django.contrib.auth.tokens import default_token_generator
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import filters, generics, mixins, status, viewsets

from .serializers import SignupSerializer, User, UserSerializer
from .utils import confirm_email_sendler


class CreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    pass


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет обрабатывающий запросы к эндпоинту 'users'."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
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


class SignupView(generics.CreateAPIView):
    """Регистрации нового пользователя и подтверждение по почте."""

    queryset = User.objects.all()
    serializer_class = SignupSerializer

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

# TODO: написать представление для авторизации токена
class ReceiveTokenView(generics.CreateAPIView):
    ...
