from core.filters import BudgetFilter
from core.models import Budget, Transaction
from core.serializers import (
    BudgetCreateSerializer,
    BudgetSerializer,
    BudgetShareSerializer,
    TransactionCreateSerializer,
    TransactionSerializer,
)
from django.contrib.auth.models import User
from django.db.models import QuerySet
from django_filters import rest_framework
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import GenericViewSet


class BudgetViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    permission_classes = (IsAuthenticated,)
    serializer_class = BudgetSerializer
    queryset = Budget.objects.all()
    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_class = BudgetFilter
    filterset_fields = ("category",)

    def create(self, request, *args, **kwargs):
        write_serializer = BudgetCreateSerializer(data=request.data)
        if write_serializer.is_valid(raise_exception=True):
            instance = write_serializer.save()
            read_serializer = self.serializer_class(instance=instance)
            return Response(read_serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=["GET"], detail=False, url_path="my-budgets")
    def my_budgets(self, request):
        user_id: str = str(request.user.id)
        user: User = User.objects.get(id=user_id)
        queryset: QuerySet = Budget.objects.filter(user=user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            data = BudgetSerializer(instance=queryset, many=True).data
            return self.get_paginated_response(data)

        serializer: ModelSerializer = BudgetSerializer(instance=queryset, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=["POST"], detail=False, url_path="share")
    def share(self, request):
        serializer = BudgetShareSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            budget_id = request.data.get("budget")
            try:
                budget = Budget.objects.get(id=budget_id)
                user_id: str = str(request.user.id)
                user: User = User.objects.get(id=user_id)
                budget.allowed_to.add(user)
                budget.save()
                return Response(f"Budget shared with user {user}", status=status.HTTP_200_OK)
            except Budget.DoesNotExist:
                return Response("There is no budget with given id")


class TransactionViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    permission_classes = (IsAuthenticated,)
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()

    def create(self, request, *args, **kwargs):
        write_serializer = TransactionCreateSerializer(data=request.data)
        if write_serializer.is_valid(raise_exception=True):
            instance = write_serializer.save()
            read_serializer = self.serializer_class(instance=instance)
            return Response(read_serializer.data, status=status.HTTP_201_CREATED)
