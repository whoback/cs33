
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("timer/new", views.create_new_timer, name="create_new_timer"),
    path("timer/<int:timer_id>", views.timer, name="timer"),
    path("timer/edit/<int:timer_id>", views.edit_timer),
    path("timer/delete/<int:timer_id>", views.delete_timer),
]
