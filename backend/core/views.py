from core.filters import BudgetFilter
from core.models import Budget
from core.serializers import BudgetSerializer
from django.contrib.auth.models import User
from django_filters import rest_framework
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet


class BudgetViewSet(
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    serializer_class = BudgetSerializer
    queryset = Budget.objects.all()
    filter_backends = (rest_framework.DjangoFilterBackend,)
    filterset_class = BudgetFilter
    filterset_fields = ("category",)
