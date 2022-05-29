import jwt

from rest_framework import serializers

from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model

from datetime import datetime, timedelta

from innotter.settings import (
    JWT_SECRET,
    JWT_ACCESS_TTL,
    JWT_REFRESH_TTL,
)

User = get_user_model()


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "role",
            "is_blocked",
        )


class UserRetrieveSerializer(serializers.ModelSerializer):
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


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, write_only=True)
    password = serializers.CharField(required=True, write_only=True)

    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def validate(self, validated_data):
        error_msg = ("email or password are incorrect")

        try:
            user = User.objects.get(email=validated_data["email"])

            if not user.check_password(validated_data["password"]):
                raise serializers.ValidationError(error_msg)

            validated_data["user"] = user

        except User.DoesNotExist:
            raise serializers.ValidationError(error_msg)

        return validated_data

    def create(self, validated_data):
        """Creating tokens for user"""

        access_payload = {
            "iss": "backend-api",
            "user_id": validated_data["user"].id,
            "exp": datetime.utcnow() + timedelta(seconds=JWT_ACCESS_TTL),
            "type": "access"
        }
        access = jwt.encode(payload=access_payload, key=JWT_SECRET)

        refresh_payload = {
            "iss": "backend-api",
            "user_id": validated_data["user"].id,
            "exp": datetime.utcnow() + timedelta(seconds=JWT_REFRESH_TTL),
            "type": "refresh"
        }

        refresh = jwt.encode(payload=refresh_payload, key=JWT_SECRET)

        return {
            "access": access,
            "refresh": refresh
        }


class RefreshTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(required=True, write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def validate(self, validated_data):
        validated_data = super().validate(validated_data)

        try:
            payload = jwt.decode(validated_data["refresh_token"], JWT_SECRET, algorithms=['HS256'])
            if payload["type"] != "refresh":
                error_msg = {"refresh_token": "Token type is not refresh!"}
                raise serializers.ValidationError(error_msg)
            validated_data["payload"] = payload

        except jwt.ExpiredSignatureError:
            error_msg = {"refresh_token": "Refresh token is expired!"}
            raise serializers.ValidationError(error_msg)

        except jwt.InvalidTokenError:
            error_msg = {"refresh_token": "Refresh token is invalid!"}
            raise serializers.ValidationError(error_msg)

        return validated_data

    def create(self, validated_data):
        """Creating tokens for user"""
        access_payload = {
            "iss": "backend-api",
            "user_id": validated_data["payload"]["user_id"],
            "exp": datetime.utcnow() + timedelta(seconds=JWT_ACCESS_TTL),
            "type": "access"
        }
        access = jwt.encode(payload=access_payload, key=JWT_SECRET)

        refresh_payload = {
            "iss": "backend-api",
            "user_id": validated_data["payload"]["user_id"],
            "exp": datetime.utcnow() + timedelta(seconds=JWT_REFRESH_TTL),
            "type": "refresh"
        }

        refresh = jwt.encode(payload=refresh_payload, key=JWT_SECRET)

        return {
            "access": access,
            "refresh": refresh
        }
