from django.contrib import admin
from .transaction import TransactionInline

class AccountAdmin(admin.ModelAdmin):
    list_display = ["label", "create_at", "isPositive"]
    fields = ["label", "balance", "create_at"]
    inlines = [TransactionInline]