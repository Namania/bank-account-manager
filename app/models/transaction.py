from django.utils import timezone
from django.db import models
from djmoney.models.fields import MoneyField
from .account import Account


class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    amount = MoneyField(max_digits=14, decimal_places=2, default_currency='EUR', default=0)
    comment = models.CharField(max_length=200)
    create_at = models.DateTimeField("Create at", default=timezone.now)
    
    def __str__(self):
        return self.account.label if self.account is not None else "deleted_account"