from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import redirect, render, get_object_or_404

from app.models import Account, Transaction

def profile(request):
    if "username" not in request.session.keys():
        return redirect("login")
    userId = request.session["id"]
    user = get_object_or_404(User, pk=userId)

    accounts = Account.objects.filter(owner=user).order_by("balance").reverse()
    transaction_count = Transaction.objects.filter(Q(sender_id=user.pk) | Q(receiver_id=user.pk)).count()

    return render(request, "app/profile.html", {"user": user, "accounts": accounts, "account_count": len(accounts), "transaction_count": transaction_count})
