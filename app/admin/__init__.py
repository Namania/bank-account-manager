from django.contrib import admin
from app.models.account import Account
from app.models.transaction import Transaction
from app.models.category import Category

from .account import AccountAdmin
from .transaction import TransactionAdmin
from .category import CategoryAdmin

admin.site.register(Account, AccountAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Category, CategoryAdmin)