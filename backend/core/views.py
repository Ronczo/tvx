from core.filters import BudgetFilter
from core.models import Budget
from core.serializers import BudgetSerializer
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
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    permission_classes = (IsAuthenticated,)
    serializer_class = BudgetSerializer
    queryset = Budget.objects.all()
    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_class = BudgetFilter
    filterset_fields = ("category",)

    @action(methods=["GET"], detail=False, url_path="my-budgets")
    def my_budgets(self, request):
        user_id: str = str(request.user.id)
        user: User = User.objects.get(id=user_id)
        queryset: QuerySet = Budget.objects.filter(user=user)
        serializer: ModelSerializer = BudgetSerializer(instance=queryset, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
