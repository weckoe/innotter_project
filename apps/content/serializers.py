from rest_framework import serializers
from apps.content.models import (
    Post,
    Tag,
    )

class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
                "__all__"
                )

class TagListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
                "__all__"
                ) 
