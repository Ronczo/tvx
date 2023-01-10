from authorization.views import UserViewSet
from core.views import BudgetViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("budget", BudgetViewSet, basename="user")
urlpatterns = router.urls
