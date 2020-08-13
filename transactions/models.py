from decimal import *

import requests
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import Q


class Transaction(models.Model):
    STATUSES = (
        ('O', 'Outgoing'),
        ('R', 'Rejected')
    )
    amount = models.IntegerField(default=0)
    destination = models.CharField(max_length=30, blank=False)
    status = models.CharField(max_length=1, default='R', choices=STATUSES)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        allow_transaction = self.__validate_policy_rule()
        if allow_transaction:
            self.status = 'O'
            super().save(self)
        else:
            super().save(self)

    def __validate_policy_rule(self):
        if PolicyRule.objects.filter(
                (Q(amount_in_satoshis=-1) & Q(destinations__contains=['any'])) |
                (Q(amount_in_satoshis=-1) & Q(destinations__contains=[self.destination])) |
                (Q(amount_in_satoshis__gt=self.amount) & Q(destinations__contains=['any'])) |
                (Q(amount_in_satoshis__gt=self.amount) & Q(destinations__contains=[self.destination]))
        ):
            return True
        return False


class PolicyRule(models.Model):
    CURRENCIES = (
        ('BTC', 'Bitcoin in satoshis'),
        ('USD', 'United States Dollar')
    )
    url = 'https://blockchain.info/tobtc'
    id = models.AutoField(primary_key=True)
    amount = models.IntegerField(default=0)
    destinations = ArrayField(
        models.CharField(max_length=30, blank=False), blank=False
    )
    currency = models.CharField(max_length=3, blank=True, null=False, default='BTC', choices=CURRENCIES)
    amount_in_satoshis = models.IntegerField(null=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.amount == -1:
            self.amount_in_satoshis = -1
            super().save()
            return
        if self.currency != 'BTC':
            params = (('currency', self.currency), ('value', self.amount))
            response = requests.get(self.url, params=params)
            if response.status_code != 200:
                message = "Currency exchange failed: " + response.text
                raise MoneyExchangeError(message=message, code=response.status_code)
            self.amount_in_satoshis = int(float(response.text) * float(100000000))
        else:
            self.amount_in_satoshis = self.amount
        super().save()


class MoneyExchangeError(Exception):
    def __init__(self, message, code=None, params=None):
        super().__init__(message, code, params)

        self.message = message
