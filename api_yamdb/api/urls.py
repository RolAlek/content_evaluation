from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.views import UserViewSet, ReviewViewSet, CommentViewSet

  
app_name = 'api'

router_v1 = SimpleRouter()
router_v1.register(prefix='users', viewset=UserViewSet)
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews',
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments',
)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
