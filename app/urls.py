from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("<int:accountId>/", views.accountView, name="account"),
    path("new-account/", views.newAccountView, name="new-account"),
    path("new-transaction/", views.newTransactionView, name="new-transaction"),
    path("user/", views.profile, name="profile"),
]
