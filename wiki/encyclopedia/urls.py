from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>", views.wiki, name="title"),
    path("wiki/<str:title>", views.wiki, name="entry")

]
