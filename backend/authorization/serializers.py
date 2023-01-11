from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]
        ref_name = "User serializer"


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password"]
        ref_name = "User create serializer"

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data.get("password"))
        return super().create(validated_data)
