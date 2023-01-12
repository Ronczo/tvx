from django.contrib import admin

from core.models import Budget, Transaction, TransactionCategory

admin.site.register(Budget)
admin.site.register(Transaction)
admin.site.register(TransactionCategory)
