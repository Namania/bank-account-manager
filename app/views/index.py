import json
import datetime

from django.contrib.auth.models import User
from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Q
from app.models import Transaction

from app.utils.account import getAccounts

def index(request):
    if "username" not in request.session.keys():
        return redirect("login")
    userId = request.session["id"]
    user = get_object_or_404(User, pk=userId)

    accounts = getAccounts(user)

    now = datetime.datetime.now()
    current_month = now.replace(day=now.day)
    month, year = (now.month - 1, now.year) if now.month != 1 else (12, now.year - 1)
    last_month = now.replace(day=now.day - 1 if now.day != 1 else now.day, month=month, year=year)

    colors = [
        "pink",
        "orange",
        "yellow",
        "light-blue",
        "blue",
        "purple",
    ]

    datasets = {
        "labels": [
        ],
        "data": [
        ],
        "color": [
        ]
    }

    account_ids = []
    totalAmount = {
        "amount": 0,
        "currency": "EUR"
    }
    index = 0
    for account in accounts:
        account_ids.append(account.pk)
        datasets["labels"].append(account.label)
        datasets["data"].append(account.getBalance())
        datasets["color"].append(colors[index % len(colors)])
        index+=1
        totalAmount["amount"] += account.getBalance()

    print(last_month, current_month)
    transactions = Transaction.objects.filter((Q(sender_id__in=account_ids) | Q(receiver_id__in=account_ids)) & Q(create_at__range=[last_month, current_month])).order_by("-create_at")[:4]
    return render(request, "app/index.html", {"accounts": accounts, "user": user, "totalAmount": totalAmount, "json": json.dumps(datasets), "transactions": transactions})
