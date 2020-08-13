from rest_framework import serializers

from .models import Transaction, PolicyRule


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction

        fields = ('amount', 'destination')


class PolicyRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PolicyRule

        fields = ('id', 'amount', 'destinations', 'currency')
