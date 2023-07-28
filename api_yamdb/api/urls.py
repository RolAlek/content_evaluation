from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import ReceiveTokenView, SignupView, UserViewSet

router_v1 = SimpleRouter()
router_v1.register(prefix='users', viewset=UserViewSet)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', SignupView.as_view()),
    path('v1/auth/token/', ReceiveTokenView.as_view())
]
