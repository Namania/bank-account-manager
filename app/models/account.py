from django.utils import timezone
from django.db import models
from django.contrib import admin
from djmoney.models.fields import MoneyField
from django.contrib.auth.models import User

class Account(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    label = models.CharField(max_length=200, verbose_name="Title")
    balance = MoneyField(max_digits=14, decimal_places=2, default_currency='EUR', default=0, verbose_name="Balance")
    create_at = models.DateTimeField(default=timezone.now, verbose_name="Create at")
    isActive = models.BooleanField(default=True, verbose_name="Is Active")

    @admin.display(
        boolean=True,
        description="Is Positive",
    )
    def isPositive(self):
        return self.balance.amount >= 0
    
    def add(self, amount: float):
        self.balance.amount += int(amount * 100)

    def remove(self, amount: float):
        self.balance.amount -= int(amount * 100)

    def getBalance(self):
        return float(int(self.balance.amount) / 100)
    
    def set(self, amount: float):
        self.balance.amount = int(amount * 100)

    def getName(self):
        return self.label if self.isActive else f"{self.label} (deleted)"
    
    def __str__(self):
        return self.label