from django.urls import path, include
from rest_framework.routers import SimpleRouter
from api.views import (
    TitleViewSet, GenreViewSet, CategoryViewSet
)

app_name = 'api'

router = SimpleRouter()
router.register(
    r'titles',
    TitleViewSet,
    basename='titles'
)
router.register(
    r'categories',
    CategoryViewSet,
    basename='category'
)
router.register(
    r'genres',
    GenreViewSet,
    basename='genres'
)

urlpatterns = [
    path('v1/', include(router.urls)),
]
