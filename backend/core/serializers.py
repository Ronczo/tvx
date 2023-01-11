from core.models import Budget, Transaction, TransactionCategory
from rest_framework import serializers


class TransactionSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="get_category")

    class Meta:
        model = Transaction
        exclude = [
            "budget",
        ]
        ref_name = "Transaction serializer"


class TransactionCreateSerializer(serializers.ModelSerializer):
    category = serializers.CharField()

    class Meta:
        model = Transaction
        fields = "__all__"
        ref_name = "Transaction serializer"

    def create(self, validated_data):
        category, _ = TransactionCategory.objects.get_or_create(name=validated_data.get("category"))
        validated_data["category"] = category
        return super().create(validated_data)


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


class BudgetShareSerializer(serializers.ModelSerializer):
    budget = serializers.CharField()

    class Meta:
        model = Budget
        fields = ["budget"]
        ref_name = "Budget serializer"


class BudgetCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = "__all__"
        ref_name = "Budget serializer"
