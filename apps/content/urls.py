from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.content.views import (
        PostViewSet, 
        TagViewSet,
    )

router = DefaultRouter()

router.register(r"posts", PostViewSet, basename="posts")
router.register(r"tags", TagViewSet, basename="tags")


urlpatterns = [
        path("", include(router.urls))
        ]
