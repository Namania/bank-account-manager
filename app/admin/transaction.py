from django.contrib import admin
from app.models import Transaction

class TransactionAdmin(admin.ModelAdmin):
    list_display = ["sender", "receiver", "amount", "comment", "category", "create_at"]
    fields = ["sender", "receiver", "amount", "comment", "category", "create_at"]

class TransactionInline(admin.TabularInline):
    model = Transaction
    fk_name = "sender"
    extra = 0