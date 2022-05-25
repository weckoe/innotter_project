from http import HTTPStatus

from rest_framework import viewsets, mixins, generics
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import ( 
    AllowAny, 
    BasePermission
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
    permission_classes = (IsAuthenticated, ) 
    authentication_classes = (JWTAuthentication,)

    def get_serializer_class(self):
        if self.action == "list" or "retrieve":
            return UserGetSerializer
        return UserGetSerializer

    def create(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.validated_data)

    def update(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        serializer = UserUpdateSerializer(data=request.data, instance=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.validated_data)

    def delete(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        user.delete()

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
