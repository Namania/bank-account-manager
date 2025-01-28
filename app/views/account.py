import json
import datetime

from django.contrib.auth.models import User
from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Q
from app.models import Account, Transaction

from app.utils.account import getAccounts


def accountView(request, accountId):
    if "username" not in request.session.keys():
        return redirect("login")
    userId = request.session["id"]
    user = get_object_or_404(User, pk=userId)

    RED = 'rgb(236, 112, 99)'
    GREEN = 'rgb(82, 190, 128)'
    BLUE = 'rgb(54, 162, 235)'
    datasets = {
        "labels": [
        ],
        "data": [
        ],
        "backgroundColor": [
        ]
    }

    accounts = getAccounts(user)
    account = get_object_or_404(Account, pk=accountId)

    transactions = Transaction.objects.filter(Q(sender=account) | Q(receiver=account)).order_by("-create_at")
    hasData = transactions.exists()
    for transaction in transactions:
        datasets["labels"].append(transaction.__str__())
        datasets["data"].append(float(transaction.amount.amount))
        if transaction.sender.owner == user and transaction.receiver.owner == user:
            color = BLUE
        elif transaction.receiver == account:
            color = GREEN
        else:
            color = RED
        datasets["backgroundColor"].append(color)

    return render(request, "app/account.html", {"user": user,"accounts": accounts, "account": account, "json": json.dumps(datasets), "transactions": transactions, "hasData": hasData})

def newAccountView(request):
    if "username" not in request.session.keys():
        return redirect("login")
    userId = request.session["id"]
    user = get_object_or_404(User, pk=userId)


    if request.method == "POST":
        account = Account.objects.create(owner=user, label=request.POST["label"], balance=0)
        account.set(float(request.POST["balance"]))
        account.save()
        return redirect("index")

    accounts = getAccounts(user)
    return render(request, "app/new-account.html", {"accounts": accounts, "user": user})

def delete(request, accountId):
    if "username" not in request.session.keys():
        return redirect("login")
    userId = request.session["id"]
    user = get_object_or_404(User, pk=userId)

    account = get_object_or_404(Account, pk=accountId)
    if account.owner == user:
        account.isActive = False
        account.save()
    return redirect("index")

def edit(request, accountId):
    if "username" not in request.session.keys():
        return redirect("login")
    userId = request.session["id"]
    user = get_object_or_404(User, pk=userId)

    accounts = getAccounts(user)
    account = get_object_or_404(Account, pk=accountId)

    if request.method == "POST":
        account.label = request.POST["label"]
        account.set(float(request.POST["balance"]))
        account.save()
        return redirect(f"/{account.pk}/")

    return render(request, "app/edit-account.html", {"account": account, "accounts": accounts, "user": user})
