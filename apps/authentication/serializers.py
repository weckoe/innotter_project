from rest_framework import serializers

from django.contrib.auth.password_validation import validate_password

from apps.authentication.models import User

class UserListRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "role",
            "title",
            "is_blocked",
            "password",
        )

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
                "username",
                "email",
                "first_name",
                "last_name",
                "title",
                )
        extra_kwargs = {
            "username": {"required": True},
            "email": {"required": True},

        }

    def update(self, instance, validated_data):
        instance.email = validated_data["email"]
        instance.username = validated_data["username"]
        instance.first_name = validated_data["first_name"]
        instance.last_name = validated_data["last_name"]
        instance.title = validated_data["title"]

        instance.save()

        return instance


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )

    class Meta:
        model = User

        fields = (
                "username",
                "email",
                "first_name",
                "last_name",
                "title",
                "role",
                "password",
                "password2"
                )

        extra_kwargs = {
            "username": {"required": True},
            "email": {"required": True},
            "password": {"required": True},
            "password2": {"required": True},    
            "role": {"required": True},
        }

    def validate(self, validated_data):
        if validated_data["password"] != validated_data["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return validated_data

    def create(self, validated_data):
        new_user = User.objects.create_user(
                username=validated_data["username"], 
                email=validated_data["email"],
                first_name=validated_data["first_name"], 
                last_name=validated_data["last_name"],
                role=validated_data["role"],
                title=validated_data['title']
                )
        new_user.set_password(validated_data['password'])

        new_user.save()

        return new_user
