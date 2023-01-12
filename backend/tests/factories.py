from random import choice, randint

import factory
from core.models import Budget, Transaction, TransactionCategory
from django.contrib.auth.models import User
from factory import Faker

KINDS = ["income", "expanse"]
CATEGORIES = ["food", "school", "tax", "home", "trip", "other"]


class TransactionCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TransactionCategory

    name = choice(CATEGORIES)


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = Faker("name")
    password = Faker("password")
    email = Faker("email")


class BudgetFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Budget

    user = factory.Iterator(User.objects.all())
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

    kind = choice(KINDS)
    value = randint(0, 100)
    budget = factory.Iterator(Budget.objects.all())
    category = factory.SubFactory(TransactionCategoryFactory)
