from core.models import Budget
from django.contrib.auth.models import User
from rest_framework import serializers


class BudgetSerializer(serializers.ModelSerializer):
    transaction = serializers.StringRelatedField(many=True)

    class Meta:
        model = Budget
        fields = "__all__"
        ref_name = "Budget serializer"
