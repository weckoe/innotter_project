from http import HTTPStatus

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import ( 
    AllowAny, 
    BasePermission
)

from apps.authentication.models import User
from apps.authentication.serializers import (
    UserListRetrieveSerializer,
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


class UserViewSet(viewsets.ViewSet, LimitOffsetPagination):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, ) 
    authentication_classes = (JWTAuthentication,)


    def list(self, request):
        results = self.paginate_queryset(self.queryset, request)
        serializer = UserListRetrieveSerializer(results, many=True)
        return self.get_paginated_response(serializer.data)

    def retrieve(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        serializer = UserListRetrieveSerializer(user)
        return Response(serializer.data)

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


class LoginViewSet(viewsets.ViewSet):
    queryset = User.objects.all()
    permission_classes = (AllowAny,) 

    def create(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response_data = serializer.save()
        return Response(response_data)

class RefreshTokenViewSet(viewsets.ViewSet):
    queryset = User.objects.all()
    permission_classes = (AllowAny,) 

    def create(self, request):
        serializer = RefreshTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response_data = serializer.save()
        return Response(response_data)
