from django.shortcuts import render, get_object_or_404

from .models import Account

def index(request):
    accounts = Account.objects.all()
    return render(request, "app/index.html", {"accounts": accounts})

def accountView(request, accountId):
    account = get_object_or_404(Account, pk=accountId)
    return render(request, "app/account.html", {"account": account})