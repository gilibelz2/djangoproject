from .api import TransactionViewSet, PolicyRuleViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter(trailing_slash=False)
router.register('transactions', TransactionViewSet, basename='transactions')
router.register('policy_rule', PolicyRuleViewSet, basename='policy_rule')
urlpatterns = router.urls
