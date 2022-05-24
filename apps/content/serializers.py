from rest_framework import serializers

from apps.content.models import (
    Post,
    Tag,
    Page,
)


class PostListRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            "content",
            "page",

        )

class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
                "content",
                "page",
        )

class PostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            "content",
        )

        def update(self, validated_data, instance):
            instance.content = validated_data["content"]

            instance.save()

            return instance

class TagListRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            "name",
        )

class TagUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            "name",
        )

    def update(self, instance, validated_data):
        instance.name = validated_data["name"]
        instance.save()

        return instance

class TagCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            "name",
        )

    def create(self, validated_data):
        new_tag = Tag.objects.create(name=validated_data["name"])
        
        return new_tag

class PageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = (
            "id",
            "name",
            "image",
            "description",
            "owner",
            "tags",
            "followers",
            "follow_requests",
        ) 

class PageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = (
                "name",
                "owner",
                "description",
                "tags",
            )
        extra_kwargs = {
            "name": {"required": True},
            "owner": {"required": True},
        }

    def create(self, validated_data):
        new_page = Page.objects.create(
                name=validated_data["name"],
                owner=validated_data["owner"],
                description=validated_data["description"],
        )
        for single_tag in validated_data["tags"]:
            new_page.tags.add(single_tag)

        new_page.save()

        return new_page

class PageUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = (
                "name",
                "owner",
                "description",
                "tags",
            )

        def update(self, validated_data, instance):
            instance.name = validated_data["name"]
            instance.owner = validated_data["owner"]
            instance.description = validated_data["description"]

            for single_tag in validated_data["tags"]:
                instance.tags.add(single_tag)

            instance.save()

            return instance
