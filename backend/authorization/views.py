from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from authorization.serializers import UserCreateSerializer, UserSerializer


class UserViewSet(
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        write_serializer = UserCreateSerializer(data=request.data)
        if write_serializer.is_valid(raise_exception=True):
            instance = write_serializer.save()
            read_serializer = self.serializer_class(instance=instance)
            return Response(read_serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        self.pagination_class = None
        return super().list(request, *args, **kwargs)
