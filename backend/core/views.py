from django.contrib.auth.models import User
from django.db.models import QuerySet
from django_filters import rest_framework
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import GenericViewSet

from core.filters import BudgetFilter
from core.models import Budget, Transaction
from core.permissions import IsBudgetSharedPermission
from core.serializers import (
    BudgetCreateSerializer,
    BudgetSerializer,
    BudgetShareSerializer,
    TransactionCreateSerializer,
    TransactionSerializer,
)


class BudgetViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet,
):
    permission_classes = (IsAuthenticated,)
    serializer_class = BudgetSerializer
    queryset = (
        Budget.objects.all().prefetch_related("transactions").select_related("user")
    )
    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_class = BudgetFilter
    filterset_fields = ("category",)

    def create(self, request, *args, **kwargs):
        write_serializer = BudgetCreateSerializer(data=request.data)
        if write_serializer.is_valid(raise_exception=True):
            instance = write_serializer.save()
            read_serializer = self.serializer_class(instance=instance)
            return Response(read_serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        self.permission_classes = [IsBudgetSharedPermission]
        return super().retrieve(request, *args, **kwargs)

    @action(methods=["GET"], detail=False, url_path="my-budgets")
    def my_budgets(self, request):
        user_id: str = str(request.user.id)
        user: User = User.objects.get(id=user_id)
        queryset: QuerySet = (
            Budget.objects.filter(user=user)
            .prefetch_related("transactions")
            .select_related("user")
        )
        filtered_qs = BudgetFilter(data=self.request.GET, queryset=queryset)

        page = self.paginate_queryset(filtered_qs.qs)
        if page is not None:
            serializer = BudgetSerializer(instance=filtered_qs.qs, many=True)
            return self.get_paginated_response(serializer.data)

        serializer: ModelSerializer = BudgetSerializer(
            instance=filtered_qs.qs, many=True
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=["POST"], detail=False, url_path="share")
    def share(self, request):
        IsBudgetSharedPermission()
        serializer = BudgetShareSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            budget_id: str = request.data.get("budget")
            user_id: str = request.data.get("user")
            try:
                budget = Budget.objects.get(id=budget_id)
                user: User = User.objects.get(id=user_id)
                budget.allowed_to.add(user)
                budget.save()
                return Response(
                    f"Budget shared with user {user}", status=status.HTTP_200_OK
                )
            except (Budget.DoesNotExist, User.DoesNotExist):
                return Response("There is no budget or User with given id")

    @action(methods=["GET"], detail=False, url_path="shared-with-me")
    def shared_with_me(self, request):
        user_id: str = str(request.user.id)
        user: User = User.objects.get(id=user_id)
        shared_budgets = (
            Budget.objects.filter(allowed_to=user)
            .prefetch_related("transactions")
            .select_related("user")
        )
        page = self.paginate_queryset(shared_budgets)
        if page is not None:
            serializer = BudgetSerializer(instance=shared_budgets, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.serializer_class(instance=shared_budgets, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TransactionViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    permission_classes = (IsAuthenticated,)
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all().select_related("category")

    def create(self, request, *args, **kwargs):
        write_serializer = TransactionCreateSerializer(data=request.data)
        if write_serializer.is_valid(raise_exception=True):
            instance = write_serializer.save()
            read_serializer = self.serializer_class(instance=instance)
            return Response(read_serializer.data, status=status.HTTP_201_CREATED)
