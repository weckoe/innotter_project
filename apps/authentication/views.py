from http import HTTPStatus

from rest_framework.decorators import action
from rest_framework import viewsets, mixins, generics
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (
    AllowAny,
    BasePermission,
)

from apps.authentication.models import User
from apps.authentication.serializers import (
    UserGetSerializer,
    UserUpdateSerializer,
    UserCreateSerializer,
    LoginSerializer,
    RefreshTokenSerializer,
)
from apps.authentication.backends import JWTAuthentication

from django.shortcuts import get_object_or_404


class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        if request.user.role == "admin" or request.user.role == "moderator":
            return True
        False


class UserViewSet(viewsets.ModelViewSet, LimitOffsetPagination):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)
    serializer_classes = {
        "list": UserGetSerializer,
        "retrieve": UserGetSerializer,
        "update": UserUpdateSerializer,
        "create": UserCreateSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, UserGetSerializer)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.validated_data)

    def update(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        serializer = self.get_serializer(data=request.data, instance=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.validated_data)

    def delete(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        user.delete()

        return Response(status=HTTPStatus.ACCEPTED)

    @action(methods=['POST', ], url_path="block-user/(?P<id>[0-9]+)", url_name="block-user", detail=False)
    def block_user(self, request, id=None):
        user = User.objects.get(pk=id)
        user.is_blocked = True
        user.save()

        return Response(status=HTTPStatus.ACCEPTED)


class LoginView(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response_data = serializer.save()

        return Response(response_data)


class RefreshTokenView(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = RefreshTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response_data = serializer.save()
        return Response(response_data)
