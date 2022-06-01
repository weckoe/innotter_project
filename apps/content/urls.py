from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.content.views import (
    PostViewSet,
    TagViewSet,
    PageViewSet,
)

app_name = "content"

router = DefaultRouter()

router.register(r"posts", PostViewSet, basename="posts")
router.register(r"tags", TagViewSet, basename="tags")
router.register(r"pages", PageViewSet, basename="pages")

urlpatterns = [
    path("api/", include(router.urls)),
    ]
