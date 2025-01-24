from django.utils import timezone
from django.db import models
from djmoney.models.fields import MoneyField

from .account import Account
from .category import Category


class Transaction(models.Model):
    sender = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, related_name="sender")
    receiver = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, related_name="receiver")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="category")
    amount = MoneyField(max_digits=14, decimal_places=2, default_currency='EUR', default=0)
    comment = models.CharField(max_length=200,null=True)
    create_at = models.DateTimeField("Create at", default=timezone.now)

    def __str__(self):
        return f"{self.sender.label} => {self.receiver.label}" if self.sender is not None and self.receiver is not None else "deleted_account"
