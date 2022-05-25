from http import HTTPStatus

from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError

from rest_framework.pagination import LimitOffsetPagination
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action

from apps.authentication.backends import JWTAuthentication

from apps.content.models import (
    Post,
    Tag,
    Page,
)
from apps.content.serializers import (
    PostGetSerializer,
    PostCreateSerializer,
    PostUpdateSerializer,
    TagGetSerializer,
    TagUpdateSerializer,
    TagCreateSerializer,
    PageGetSerializer,
    PageCreateSerializer,
    PageUpdateSerializer,
)


class PostViewSet(viewsets.ViewSet, LimitOffsetPagination):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)
    queryset = Post.objects.all()

    def list(self, request):
        results = self.paginate_queryset(self.queryset, request)
        serializer = PostListRetrieveSerializer(results, many=True)
        return self.get_paginated_response(serializer.data)

    def retrieve(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        serializer = PostListRetrieveSerializer(post)
        return Response(serializer.data)

    def create(self, request):
        serializer = PostCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=HTTPStatus.ACCEPTED)

    def update(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        serializer = PostUpdateSerializer(data=request.data, instance=post)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=HTTPStatus.ACCEPTED)

    def delete(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)

        if request.user.id == Page.objects.get(id=post.page_id).owner_id:
            post.delete()
            return Response(status=HTTPStatus.ACCEPTED)
        raise ValidationError("this not your post")


class TagViewSet(viewsets.ViewSet, LimitOffsetPagination):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)
    queryset = Tag.objects.all()

    def list(self, request):
        results = self.paginate_queryset(self.queryset, request)
        serializer = TagGetSerializer(results, many=True)

        return self.get_paginated_response(serializer.data)

    def retrieve(self, request, pk=None):
        tag = Tag.objects.get(id=pk)
        serializer = TagGetSerializer(tag)

        return Response(serializer.data)

    def update(self, request, pk=None):
        tag = get_object_or_404(Tag, id=pk)
        serializer = TagUpdateSerializer(data=request.data, instance=tag)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.validated_data["name"])

    def create(self, request, pk=None):
        serializer = TagCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.validated_data)

    def delete(self, request, pk=None):
        if request.user.role == "admin" or request.user.role == "moderator":
            tag = get_object_or_404(Tag, pk=pk)
            tag.delete()

            return Response(status=HTTPStatus.ACCEPTED)
        raise ValidationError("permission denied")


class PageViewSet(viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)
    queryset = Page.objects.all()

    def get_serializer_class(self):

        if self.action == "list" or "retrieve":
            return PageGetSerializer
        return PageGetSerializer

    @action(methods=['POST', ], url_path="follow", url_name="follow", detail=False)
    def follow(self, request):
        # page = Page.objects.get(id=pk)
        page.follow_requests.add(request.user.id)

        page.save()

        return Response(page.follow_requests)

    # def create(self, request):
    #     serializer = PageCreateSerializer(data=request.data)
    #     if serializer.is_valid(raise_exception=True):
    #         serializer.save()
    #         return Response(serializer.validated_data["name"])
    #
    # def update(self, request, pk=None):
    #     page = get_object_or_404(Page, pk=pk)
    #
    #     if request.user.id == page.owner_id:
    #         serializer = PageUpdateSerializer(data=request.data, instance=page)
    #         serializer.is_valid(raise_exception=True)
    #         serializer.save()
    #         return Response(serializer.validated_data["name"])
    #     raise ValidationError("this is not you page")
    #
    # def delete(self, request, pk=None):
    #     page = get_object_or_404(Page, pk=pk)
    #
    #     if request.user.id == page.owner_id:
    #         page.delete()
    #
    #         return Response(status=HTTPStatus.ACCEPTED)
    #     raise ValidationError("this not your page")
