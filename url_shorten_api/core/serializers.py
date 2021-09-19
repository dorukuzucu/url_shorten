from rest_framework import serializers
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from .models import User
from .models import ShortenedUrl


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "username", "fullname", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['email'], validated_data['username'],
                                        validated_data['fullname'], validated_data['password'])
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "username", "fullname")


class ShortenBodySerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortenedUrl
        fields = ("id", "original_url", "shortened_url")

    def validate(self, data):
        url_validator = URLValidator()
        if len(data["shortened_url"]) > 10:
            raise serializers.ValidationError
        try:
            url_validator(data["original_url"])
        except ValidationError:
            raise serializers.ValidationError("Invalid URL to Shorten")
        return data


class ShortenUrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortenedUrl
        fields = ("id", "user", "original_url", "shortened_url")
