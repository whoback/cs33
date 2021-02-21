from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.query, name="query"),
    path("random", views.random, name="random"),
    path("newpage", views.newpage, name="newpage"),


]
