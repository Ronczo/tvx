import uuid

from django.contrib.auth.models import User
from django.db import models


class Budget(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, related_name="budget", on_delete=models.CASCADE)
    allowed_to = models.ManyToManyField(User, related_name="budgets", null=True, blank=True)

    def __str__(self):
        return f"Budget of {self.user.username}"


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
    budget = models.ForeignKey(Budget, related_name="budget", on_delete=models.PROTECT)
    category = models.ForeignKey(
        TransactionCategory, related_name="category", on_delete=models.PROTECT
    )

    def __str__(self):
        return f"{self.value}$ {self.kind} in {self.budget.user}' budget"
