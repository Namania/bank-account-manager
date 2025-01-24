from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User

from app.models import Category, Account

def categoryIndex(request):
    if "username" not in request.session.keys():
        return redirect("login")
    userId = request.session["id"]
    user = get_object_or_404(User, pk=userId)

    accounts = Account.objects.filter(owner=user).order_by("balance").reverse()
    categories = Category.objects.all()
    return render(request, "app/category.html", {"accounts": accounts, "categories": categories, "user": user})