import uuid

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum


class Budget(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, related_name="budgets", on_delete=models.CASCADE)
    allowed_to = models.ManyToManyField(User, related_name="budget", null=True, blank=True)

    def __str__(self):
        return f"Budget of {self.user.username}"

    @property
    def budget_balance(self):
        transactions = Transaction.objects.filter(budget=self)
        incomes_value = transactions.filter(kind="income").aggregate(value=Sum("value"))
        expanes_value = transactions.filter(kind="expanse").aggregate(value=Sum("value"))
        return incomes_value["value"] - expanes_value["value"]


class TransactionType(models.TextChoices):
    PL = "income", ("income")
    EN = "expanse", ("expanse")


class TransactionCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    value = models.PositiveIntegerField(default=0)
    kind = models.CharField(
        null=False,
        max_length=7,
        choices=TransactionType.choices,
    )
    budget = models.ForeignKey(Budget, related_name="transaction", on_delete=models.PROTECT)
    category = models.ForeignKey(
        TransactionCategory, related_name="transaction", on_delete=models.PROTECT
    )

    def __str__(self):
        return f"{self.value}$ {self.kind} in {self.budget.user}' budget"

    @property
    def get_category(self):
        return self.category.name
