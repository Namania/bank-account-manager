from django.shortcuts import render

from .models import Account

# Create your views here.
def index(request):
    latest_question_list = Account.objects.order_by("-create_at")[:5]
    context = {"latest_question_list": latest_question_list}
    return render(request, "index.html", context)