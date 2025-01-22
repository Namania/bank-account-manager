import json

from django.contrib.auth.models import User
from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Q
from app.models import Account, Transaction


def accountView(request, accountId):
    if "username" not in request.session.keys():
        return redirect("login")
    userId = request.session["id"]
    user = get_object_or_404(User, pk=userId)

    RED = 'rgb(233, 24, 69)'
    GREEN = 'rgb(36, 202, 14)'
    BLUE = 'rgb(0, 123, 255)'
    datasets = {
        "labels": [
        ],
        "data": [
        ],
        "backgroundColor": [
        ]
    }

    accounts = Account.objects.filter(owner=user).order_by("balance").reverse()
    account = get_object_or_404(Account, pk=accountId)

    transactions = Transaction.objects.filter(Q(sender=account) | Q(receiver=account)).order_by("-create_at")
    hasData = transactions.exists()
    for transaction in transactions:
        datasets["labels"].append(transaction.__str__())
        datasets["data"].append(int(transaction.amount.amount))
        if transaction.sender.owner == user and transaction.receiver.owner == user:
            color = BLUE
        elif transaction.receiver == account:
            color = GREEN
        else:
            color = RED
        datasets["backgroundColor"].append(color)

    return render(request, "app/account.html", {"userId": userId,"accounts": accounts, "account": account, "json": json.dumps(datasets), "transactions": transactions[:4], "hasData": hasData})

def newAccountView(request):
    if "username" not in request.session.keys():
        return redirect("login")
    userId = request.session["id"]
    user = get_object_or_404(User, pk=userId)


    if request.method == "POST":
        Account.objects.create(owner=user, label=request.POST["label"], balance=request.POST["balance"])
        return redirect("index")

    accounts = Account.objects.filter(owner=user).order_by("balance").reverse()
    return render(request, "app/new-account.html", {"accounts": accounts})
