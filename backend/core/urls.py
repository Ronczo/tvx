from authorization.views import UserViewSet
from core.views import BudgetViewSet, TransactionViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("budget", BudgetViewSet, basename="user")
router.register("transaction", TransactionViewSet, basename="transaction")
urlpatterns = router.urls
