from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.views import (
    ReviewViewSet, CommentViewSet, TitleViewSet, GenreViewSet,
    CategoryViewSet, ReceiveTokenView, SignupView, UserViewSet
)

app_name = 'api'

router_v1 = SimpleRouter()
router_v1.register(
    r'titles',
    TitleViewSet,
    basename='titles'
)
router_v1.register(
    r'categories',
    CategoryViewSet,
    basename='category'
)
router_v1.register(
    r'genres',
    GenreViewSet,
    basename='genres'
)
router_v1.register(prefix='users', viewset=UserViewSet)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews',
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments',
)

auth_patterns = [
    path('signup/', SignupView.as_view()),
    path('token/', ReceiveTokenView.as_view()),
]
urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/', include(auth_patterns)),
]
