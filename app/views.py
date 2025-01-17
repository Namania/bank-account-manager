from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import authenticate

from .models import Account

def index(request):
    if "username" not in request.session.keys():
        return redirect("login")
    userId = request.session["id"]
    accounts = Account.objects.all()

    totalAmount = 0
    for account in accounts:
        totalAmount += account.balance.amount

    return render(request, "app/index.html", {"accounts": accounts, "userId": userId, "totalAmount": totalAmount})

def accountView(request, accountId):
    if "username" not in request.session.keys():
        return redirect("login")
    account = get_object_or_404(Account, pk=accountId)
    return render(request, "app/account.html", {"account": account})

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