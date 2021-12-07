from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("messages", views.messages, name="messages"),
    path("register", views.register, name="register"),
    path("save", views.save, name="save"),
    path("work", views.work_switch, name="work"),
    path("work/<str:type>", views.work, name="work_by_type"),
    path("account", views.account, name="account"),
    path("finance", views.finance, name="finance"),
]
