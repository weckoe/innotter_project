from django.urls import path, include

from rest_framework.routers import DefaultRouter

from apps.authentication.views import (
    UserViewSet, 
    LoginViewSet,
    RefreshTokenViewSet,
)

router = DefaultRouter()

router.register(r"users", UserViewSet, basename="users")
router.register(r"login", LoginViewSet, basename="login")
router.register(r"refresh", RefreshTokenViewSet, basename="refresh")

urlpatterns = [
    path("", include(router.urls))
]
