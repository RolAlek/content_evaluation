from rest_framework.decorators import action
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import filters

from .serializers import User
from .serializers import UserSerializer


class RetriveUpdateViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    pass


class UserViewSet(viewsets.ModelViewSet):
    """Набор представлений обрабатывающий запросы к эндпоинту 'users'."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    def get_instance(self):
        return self.request.user

    @action(methods=['get', 'patch'], detail=False)
    def me(self, request, *args, **kwargs):
        """Маршрутизация дополнительных действий при GET-, PATCH-запросах
         к api/v1/users/me/.

        При GET-запросе к эндпоинту получение данных своей учетной записи.
        При PATCH-запросе изменение данных своей учетной записи.
        """

        self.get_object = self.get_instance
        if request.method == "GET":
            return self.retrieve(request, *args, **kwargs)
        elif request.method == "PATCH":
            return self.partial_update(request, *args, **kwargs)
