from django.contrib import admin
from app.models import Transaction

class TransactionAdmin(admin.ModelAdmin):
    list_display = ["account", "amount", "comment", "create_at"]
    fields = ["account", "amount", "comment", "create_at"]

class TransactionInline(admin.TabularInline):
    model = Transaction
    extra = 0