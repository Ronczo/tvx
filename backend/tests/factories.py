from random import randint

import factory.fuzzy
from django.contrib.auth.models import User

from core.models import Budget, Transaction, TransactionCategory

KINDS = ("income", "expanse")
CATEGORIES = ["food", "school", "tax", "home", "trip", "other"]


class TransactionCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TransactionCategory

    @factory.post_generation
    def name(self, name, extracted, **kwargs):
        self.name = extracted


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("name")
    password = factory.Faker("password")
    email = factory.Faker("email")


class BudgetFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Budget

    user = factory.SubFactory(UserFactory)
    name = f"test{randint(0,20)}"

    @factory.post_generation
    def allowed_to(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for group in extracted:
                self.allowed_to.add(group)


class TransactionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Transaction

    kind = factory.fuzzy.FuzzyChoice(KINDS)
    value = factory.fuzzy.FuzzyInteger(0, 100)
    budget = factory.SubFactory(BudgetFactory)
    category = factory.fuzzy.FuzzyChoice(TransactionCategory.objects.all())
