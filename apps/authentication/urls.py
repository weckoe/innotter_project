from django.urls import path, include

from rest_framework.routers import DefaultRouter

from apps.authentication.views import (
    UserViewSet, 
    LoginView,
    RefreshTokenView,
)

router = DefaultRouter()

router.register(r"users", UserViewSet, basename="users")

urlpatterns = [
    path("", include(router.urls)),
    path("login/", LoginView.as_view(), name="login"),
    path("refresh/", RefreshTokenView.as_view(), name="refresh")
]
