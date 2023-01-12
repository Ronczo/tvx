from rest_framework.routers import DefaultRouter
from core.views import BudgetViewSet, TransactionViewSet

router = DefaultRouter()
router.register("budget", BudgetViewSet, basename="user")
router.register("transaction", TransactionViewSet, basename="transaction")
urlpatterns = router.urls
