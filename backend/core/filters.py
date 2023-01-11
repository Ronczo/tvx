import django_filters
from core.models import Budget


class BudgetFilter(django_filters.FilterSet):
    """Filter budget by category if any transaction in Budget includes given category"""

    category = django_filters.CharFilter(
        lookup_expr="icontains", field_name="transactions__category__name"
    )

    class Meta:
        model = Budget
        fields = ["category"]
