from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User

from app.models import Account, Transaction, Category
from app.utils.account import getAccounts

def transactions(request):
    if "username" not in request.session.keys():
        return redirect("login")
    userId = request.session["id"]
    user = get_object_or_404(User, pk=userId)

    accounts = getAccounts(user)
    transaction = Transaction.objects.all().order_by("-create_at")

    return render(request, "app/transaction.html", {
        "user": user,
        "accounts": accounts,
        "transactions": transaction
    })

def transactionDetail(request, transactionId):
    if "username" not in request.session.keys():
        return redirect("login")
    userId = request.session["id"]
    user = get_object_or_404(User, pk=userId)

    accounts = getAccounts(user)
    transaction = get_object_or_404(Transaction, pk=transactionId)
    categories = Category.objects.all().order_by("label")

    if request.method == "POST":

        sender = transaction.sender
        receiver = transaction.receiver
        oldAmount = transaction.amount.amount
        transaction.amount.amount = request.POST["amount"]
        transaction.comment = request.POST["description"]
        transaction.category = Category.objects.get(pk=request.POST["category"]) if request.POST["category"] != "" else None

        if sender.label != "Bank":
            sender.add(float(oldAmount))
            sender.remove(float(transaction.amount.amount))
        if receiver.label != "Bank":
            receiver.remove(float(oldAmount))
            receiver.add(float(transaction.amount.amount))

        sender.save()
        receiver.save()
        transaction.save()

        return redirect(f"/transaction/{transaction.pk}/")

    return render(request, "app/transaction-detail.html", {
        "user": user,
        "accounts": accounts,
        "transaction": transaction,
        "categories": categories
    })

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
            sender.remove(float(amount))
        if receiver.label != "Bank":
            receiver.add(float(amount))

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
