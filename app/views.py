import json

from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import authenticate

from django.contrib.auth.models import User

from .models import Account

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

    totalAmount = 0
    for account in accounts:
        datasets["labels"].append(account.label)
        datasets["data"].append(int(account.balance.amount))
        datasets["backgroundColor"].append(GREEN if account.isPositive() else RED)
        totalAmount += account.balance

    return render(request, "app/index.html", {"accounts": accounts, "userId": userId, "totalAmount": totalAmount, "json": json.dumps(datasets)})

def accountView(request, accountId):
    if "username" not in request.session.keys():
        return redirect("login")
    account = get_object_or_404(Account, pk=accountId)
    return render(request, "app/account.html", {"account": account})

def newAccountView(request):
    if "username" not in request.session.keys():
        return redirect("login")
    userId = request.session["id"]
    user = get_object_or_404(User, pk=userId)


    if request.method == "POST":
        Account.objects.create(owner=user, label=request.POST["label"], balance=request.POST["balance"])
        return redirect("index")

    accounts = Account.objects.filter(owner=user)
    return render(request, "app/new-account.html", {"accounts": accounts})

def login(request):
    error = False
    if request.method == "POST":
        user = authenticate(username=request.POST["username"], password=request.POST["password"])
        if user is not None and not (user.is_staff or user.is_superuser):
            data = user.__dict__
            request.session["username"] = data["username"]
            request.session["password"] = data["password"]
            request.session["id"] = data["id"]
            return redirect("index")
        else:
            error = True
    return render(request, "app/login.html", {"error": error})

def logout(request):
    del request.session["username"]
    del request.session["password"]
    return redirect("login")