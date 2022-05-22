from rest_framework.pagination import LimitOffsetPagination
from rest_framework import viewsets

from apps.content.models import (
    Post,
    Tag,
)
from apps.content.serializers import (
    PostListSerializer,
    TagListSerializer,
)


class PostViewSet(viewsets.ViewSet, LimitOffsetPagination):
    queryset = Post.objects.all()

    def list(self, request):
        results = self.paginate_queryset(self.queryset, request)
        serializer = PostListSerializer(results, many=True)
        return self.get_paginated_response(serializer.data)


class TagViewSet(viewsets.ViewSet, LimitOffsetPagination):
    queryset = Tag.objects.all()

    def list(self, request):
        results = self.paginate_queryset(self.queryset, request)
        serializer = TagListSerializer(results, many=True)
        return self.get_paginated_response(serializer.data)
