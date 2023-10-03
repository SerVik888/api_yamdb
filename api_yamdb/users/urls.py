from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import ConfirmCodeTokenView, RegistrationViewSet, UserViewSet

router_v1 = DefaultRouter()

router_v1.register('users', UserViewSet, basename='users')
# router_v1.register(r'me', UserViewSet, basename='me')
router_v1.register('auth/signup', RegistrationViewSet, basename='register')

urlpatterns = [
    path('', include(router_v1.urls)),
    path('auth/token/', ConfirmCodeTokenView.as_view(),
         name='get_token'),
]
