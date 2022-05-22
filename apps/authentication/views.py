from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination

from apps.authentication.models import User
from apps.authentication.serializers import (
    UserListRetrieveSerializer,
    UserUpdateSerializer,
    UserCreateSerializer,
)

from django.shortcuts import get_object_or_404


class UserViewSet(viewsets.ViewSet, LimitOffsetPagination):
    queryset = User.objects.all()

    def list(self, request):
        results = self.paginate_queryset(self.queryset, request)
        serializer = UserListRetrieveSerializer(results, many=True)
        return self.get_paginated_response(serializer.data)

    def retrieve(self, request, pk=None):
        user = get_object_or_404(self.queryset, pk=pk)
        serializer = UserListRetrieveSerializer(user)
        return Response(serializer.data)

    def create(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.validated_data)

    def update(self, request, pk=None):
        user = get_object_or_404(self.queryset, pk=pk)
        serializer = UserUpdateSerializer(data=request.data, instance=user)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.validated_data)
