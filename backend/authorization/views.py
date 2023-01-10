from authorization.serializers import UserSerializer
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet


class UserViewSet(
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    serializer_class = UserSerializer
    queryset = User.objects.all()
