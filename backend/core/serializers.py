from core.models import Budget, Transaction
from rest_framework import serializers


class TransactionSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="get_category")

    class Meta:
        model = Transaction
        exclude = [
            "budget",
        ]
        ref_name = "Transaction serializer"


class BudgetSerializer(serializers.ModelSerializer):
    transactions = TransactionSerializer(many=True)
    balance = serializers.IntegerField(source="budget_balance")
    user = serializers.CharField(source="get_username")

    class Meta:
        model = Budget
        exclude = [
            "allowed_to",
        ]
        ref_name = "Budget serializer"


class BudgetCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = "__all__"
        ref_name = "Budget serializer"
