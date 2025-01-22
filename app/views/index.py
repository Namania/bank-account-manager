import json
import datetime

from django.contrib.auth.models import User
from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Q
from app.models import Account, Transaction

def index(request):
    if "username" not in request.session.keys():
        return redirect("login")
    userId = request.session["id"]
    user = get_object_or_404(User, pk=userId)

    accounts = Account.objects.filter(owner=user).order_by("balance").reverse()

    RED = 'rgb(233, 24, 69)'
    GREEN = 'rgb(36, 202, 14)'
    datasets = {
        "labels": [
        ],
        "data": [
        ],
        "backgroundColor": [
        ]
    }

    account_ids = []
    totalAmount = 0
    for account in accounts:
        account_ids.append(account.pk)
        datasets["labels"].append(account.label)
        datasets["data"].append(int(account.balance.amount))
        datasets["backgroundColor"].append(GREEN if account.isPositive() else RED)
        totalAmount += account.balance

    now = datetime.datetime.now()
    current_month = now.replace(day=1)
    month, year = (now.month - 1, now.year) if now.month != 1 else (12, now.year - 1)
    last_month = now.replace(day=1, month=month, year=year)

    transactions = Transaction.objects.filter(Q(sender__in=account_ids) | Q(receiver__in=account_ids) & Q(create_at__range=[last_month, current_month])).order_by("-create_at")[:5]
    return render(request, "app/index.html", {"accounts": accounts, "user": user, "totalAmount": totalAmount, "json": json.dumps(datasets), "transactions": transactions})
