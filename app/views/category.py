from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User

from app.models import Category
from app.utils.account import getAccounts

def categoryIndex(request):
    if "username" not in request.session.keys():
        return redirect("login")
    userId = request.session["id"]
    user = get_object_or_404(User, pk=userId)

    accounts = getAccounts(user)
    categories = Category.objects.all()
    return render(request, "app/category.html", {"accounts": accounts, "categories": categories, "user": user})

def categoryDetail(request, categoryId):
    if "username" not in request.session.keys():
        return redirect("login")
    userId = request.session["id"]
    user = get_object_or_404(User, pk=userId)

    accounts = getAccounts(user)
    category = get_object_or_404(Category, pk=categoryId)

    if request.method == "POST":
        category.label = request.POST["label"]
        category.color = request.POST["color"]
        category.save()

    return render(request, "app/category-detail.html", {"accounts": accounts, "category": category, "user": user})

def newCategory(request):
    if "username" not in request.session.keys():
        return redirect("login")
    userId = request.session["id"]
    user = get_object_or_404(User, pk=userId)

    if request.method == "POST":
        Category.objects.create(label=request.POST["label"], color=request.POST["color"])
        return redirect("/category/")

    accounts = getAccounts(user)
    return render(request, "app/new-category.html", {"accounts": accounts, "user": user})
