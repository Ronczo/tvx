# Generated by Django 4.1.5 on 2023-01-11 17:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0004_budget_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="transaction",
            name="budget",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="transactions",
                to="core.budget",
            ),
        ),
    ]
