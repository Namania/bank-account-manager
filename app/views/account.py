from django.contrib.auth.models import User
from django.shortcuts import redirect, render, get_object_or_404
from app.models import Account


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

    accounts = Account.objects.filter(owner=user).order_by("balance").reverse()
    return render(request, "app/new-account.html", {"accounts": accounts})
