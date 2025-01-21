from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User
from app.models import Account

def newTransactionView(request):
    if "username" not in request.session.keys():
        return redirect("login")
    userId = request.session["id"]
    user = get_object_or_404(User, pk=userId)

    accountId = int(request.GET["id"]) if request.method == "GET" and "id" in request.GET.keys() and request.GET["id"].isnumeric() else ""

    accounts = Account.objects.filter(owner=user).order_by("balance").reverse()
    return render(request, "app/new-transaction.html", {"accounts": accounts, "accountId": accountId})
