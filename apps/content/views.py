from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.decorators import action

from apps.authentication.backends import JWTAuthentication

from apps.content.models import (
    Post,
    Tag,
    Page,
)

from apps.content.serializers import (
    PostListSerializer,
    PostRetrieveSerializer,
    PostCreateSerializer,
    PostUpdateSerializer,
    TagListAndRetrieveSerializer,
    TagUpdateSerializer,
    TagCreateSerializer,
    PageListSerializer,
    PageRetrieveSerializer,
    PageCreateSerializer,
    PageUpdateSerializer,
)

User = get_user_model()


class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        if request.user.role == "admin" or "moderator":
            return True
        return False


class PostViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
):
    permission_classes = (IsAdminUser | IsAuthenticated)
    authentication_classes = (JWTAuthentication,)
    queryset = Post.objects.all()
    serializer_classes = {
        "list": PostListSerializer,
        "retrieve": PostRetrieveSerializer,
        "update": PostUpdateSerializer,
        "create": PostCreateSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, PostListSerializer)

    @action(methods=['GET', ], url_path="followed-pages-posts", url_name="followed-pages-posts", detail=False)
    def list_followed_pages_posts(self, request):
        posts = Post.objects.filter(
            page_id__in=[page.id for page in Page.objects.all().filter(followers=request.user.id)])
        serializer = self.get_serializer(posts, many=True)

        return Response(data=serializer.data)

    def update(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        serializer = self.get_serializer(data=request.data, instance=post)
        serializer.is_valid(raise_exception=True)

        return Response(status=status.HTTP_202_ACCEPTED)

    def delete(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)

        if request.user.id == Page.objects.get(id=post.page_id).owner_id:
            post.delete()
            return Response(status=status.HTTP_202_ACCEPTED)
        raise ValidationError("this not your post")


class TagViewSet(viewsets.GenericViewSet,
                 mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 mixins.CreateModelMixin,
                 mixins.UpdateModelMixin,
                 ):
    permission_classes = [IsAuthenticated | IsAdminUser]
    authentication_classes = (JWTAuthentication,)
    queryset = Tag.objects.all()
    serializer_classes = {
        "list": TagListAndRetrieveSerializer,
        "retrieve": TagListAndRetrieveSerializer,
        "update": TagUpdateSerializer,
        "create": TagCreateSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, TagListAndRetrieveSerializer)

    def update(self, request, pk=None):
        tag = get_object_or_404(Tag, id=pk)
        serializer = self.get_serializer(data=request.data, instance=tag)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.validated_data["name"], status=status.HTTP_202_ACCEPTED)

    def delete(self, request, pk=None):
        if request.user.role == "admin" or request.user.role == "moderator":
            tag = get_object_or_404(Tag, pk=pk)
            tag.delete()

            return Response(status=status.HTTP_202_ACCEPTED)
        raise ValidationError("permission denied")


class PageViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
):
    permission_classes = [IsAuthenticated | IsAdminUser]
    authentication_classes = (JWTAuthentication,)
    queryset = Page.objects.all()
    serializer_classes = {
        "list": PageListSerializer,
        "retrieve": PageRetrieveSerializer,
        "update": PageUpdateSerializer,
        "create": PageCreateSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, PageListSerializer)

    @action(methods=['POST', ], url_path="make-page-private/(?P<uuid>[\w-]+)", url_name="make-page-private",
            detail=False)
    def make_page_private(self, request, uuid=None):
        page = Page.objects.get(id=uuid)
        if request.user.id == page.owner_id:
            page.is_private = True
            page.save()

            return Response(status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

    @action(methods=['GET', ], url_path="follow/(?P<uuid>[\w-]+)", url_name="follow", detail=False)
    def follow(self, request, uuid=None):
        page = Page.objects.get(id=uuid)
        page.follow_requests.add(request.user.id)

        page.save()

        return Response(status=status.HTTP_202_ACCEPTED)

    @action(methods=['POST', ], url_path="accept-follow/(?P<uuid>[\w-]+)", url_name="follow", detail=False)
    def accept_follow(self, request, uuid=None):
        page = Page.objects.get(id=uuid)
        if request.user.id == page.owner_id:
            for user in request.data["unfollowed_users"]:
                follower_object = User.objects.get(id=user)
                page.followers.add(follower_object)
                page.follow_requests.remove(follower_object)
            page.save()

            return Response(status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

    def update(self, request, pk=None):
        page = get_object_or_404(Page, pk=pk)

        if request.user.id == page.owner_id:
            serializer = self.get_serializer(data=request.data, instance=page)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.validated_data["name"])
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

    def delete(self, request, pk=None):
        page = get_object_or_404(Page, pk=pk)
        if request.user.id == page.owner_id:
            page.delete()

            return Response(status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
