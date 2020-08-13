from django.http import HttpResponseServerError
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Transaction, PolicyRule, MoneyExchangeError
from .serializers import TransactionSerializer, PolicyRuleSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.filter(status='O')
    serializer_class = TransactionSerializer


class PolicyRuleViewSet(ModelViewSet):
    queryset = PolicyRule.objects.all()
    serializer_class = PolicyRuleSerializer

    def create(self, request, *args, **kwargs):
        try:
            serializer = PolicyRuleSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except MoneyExchangeError as e:
            return HttpResponseServerError(e.message)


