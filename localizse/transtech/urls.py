from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("log", views.log, name="log"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("messages", views.messages, name="messages"),
    path("message/<int:ID>", views.message, name="message"),
    path("register", views.register, name="register"),
    path("save", views.save, name="save"),
    path("report", views.report, name="report"),
    path("update", views.update, name="update"),
    path("users", views.users, name="users"),
    path("offer", views.offer, name="offer"),
    path("accept/<uuid:offer_id>", views.accept, name="accept"),
    path("work", views.work_switch, name="work"),
    path("work/<str:w_type>", views.work, name="work_by_type"),
    path("account", views.account, name="account"),
    path("setlang", views.set_lang, name="set_lang"),
]
