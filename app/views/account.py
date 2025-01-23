import json
import datetime

from django.contrib.auth.models import User
from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Q
from app.models import Account, Transaction


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

    accounts = Account.objects.filter(owner=user).order_by("balance").reverse()
    account = get_object_or_404(Account, pk=accountId)

    now = datetime.datetime.now()
    current_month = now
    month, year = (now.month - 1, now.year) if now.month != 1 else (12, now.year - 1)
    day = now.day - 1 if now.day != 1 else 1
    last_month = now.replace(day=day, month=month, year=year)

    transactions = Transaction.objects.filter(Q(sender=account) | Q(receiver=account) & Q(create_at__range=[last_month, current_month])).order_by("-create_at")
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

    return render(request, "app/account.html", {"user": user,"accounts": accounts, "account": account, "json": json.dumps(datasets), "transactions": transactions, "hasData": hasData})

def newAccountView(request):
    if "username" not in request.session.keys():
        return redirect("login")
    userId = request.session["id"]
    user = get_object_or_404(User, pk=userId)


    if request.method == "POST":
        Account.objects.create(owner=user, label=request.POST["label"], balance=request.POST["balance"])
        return redirect("index")

    accounts = Account.objects.filter(owner=user).order_by("balance").reverse()
    return render(request, "app/new-account.html", {"accounts": accounts, "user": user})
