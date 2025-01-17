from django.utils import timezone
from django.db import models
from django.contrib import admin
from djmoney.models.fields import MoneyField

class Account(models.Model):
    label = models.CharField(max_length=200, verbose_name="Title")
    balance = MoneyField(max_digits=14, decimal_places=2, default_currency='EUR', default=0, verbose_name="Balance")
    create_at = models.DateTimeField(default=timezone.now, verbose_name="Create at")


    @admin.display(
        boolean=True,
        description="Is Positive",
    )
    def isPositive(self):
        return self.balance.amount > 0
    
    def __str__(self):
        return self.label