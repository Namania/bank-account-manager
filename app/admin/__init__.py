from django.contrib import admin
from app.models.account import Account
from app.models.transaction import Transaction

from .account import AccountAdmin
from .transaction import TransactionAdmin

admin.site.register(Account, AccountAdmin)
admin.site.register(Transaction, TransactionAdmin)