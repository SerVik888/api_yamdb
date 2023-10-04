from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import (
    ConfirmCodeTokenViewSet,
    RegistrationViewSet,
    UserViewSet
)

router_v1 = DefaultRouter()

router_v1.register('users', UserViewSet, basename='users')
router_v1.register('auth/signup', RegistrationViewSet, basename='register')
router_v1.register('auth/token', ConfirmCodeTokenViewSet, basename='get_token')

urlpatterns = [
    path('', include(router_v1.urls)),
]
