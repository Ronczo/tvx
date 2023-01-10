from core.models import Budget, Transaction
from django.contrib.auth.models import User
from rest_framework import serializers


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"
        ref_name = "Transaction serializer"


class BudgetSerializer(serializers.ModelSerializer):
    transaction = TransactionSerializer(many=True)

    class Meta:
        model = Budget
        fields = "__all__"
        ref_name = "Budget serializer"
