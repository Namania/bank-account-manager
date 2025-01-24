from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User

from app.models import Account, Transaction, Category
from app.utils.account import getAccounts

def newTransactionView(request):
    if "username" not in request.session.keys():
        return redirect("login")
    userId = request.session["id"]
    user = get_object_or_404(User, pk=userId)

    accountId = int(request.GET["id"]) if "id" in request.GET.keys() and request.GET["id"].isnumeric() else ""

    if request.method == "POST":
        sender = Account.objects.get(pk=request.POST["sender"])
        receiver = Account.objects.get(pk=request.POST["receiver"])
        amount = request.POST["amount"]
        comment = request.POST["description"]
        category = Category.objects.get(pk=request.POST["category"]) if request.POST["category"] != "" else None

        if sender.label != "Bank":
            sender.balance.amount -= int(amount)
        if receiver.label != "Bank":
            receiver.balance.amount += int(amount)

        sender.save()
        receiver.save()

        Transaction.objects.create(sender=sender, receiver=receiver, amount=amount, comment=comment, category=category)
        if "url" in request.GET.keys() and request.GET["url"] == "account":
            return redirect("account", accountId=accountId)
        else:
            return redirect("index")

    bank = request.GET["bank"] if request.method == "GET" and "bank" in request.GET.keys() else None

    sender = Account.objects.get(pk=accountId) if accountId != "" else None
    receiver = None

    if bank is not None:
        receiver = Account.objects.get(label="Bank")
        if bank == "credit":
            sender, receiver = receiver, sender

    accounts = getAccounts(user)
    categories = Category.objects.all().order_by("label")
    return render(request, "app/new-transaction.html", {
        "user": user,
        "accounts": accounts,
        "accountId": accountId,
        "sender": sender,
        "receiver": receiver,
        "categories": categories,
    })
