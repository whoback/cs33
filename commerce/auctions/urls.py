from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path(r"listing/<uuid:id>", views.listing, name="listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("addcategory", views.addcategory, name="addcategory"),
    path("category", views.category, name="category"),
    path(r"category/<str:category_type>/list", views.category, name="category"),
    path("bid", views.bid, name="bid"),
    path("add_comment", views.add_comment, name="add_comment")

]
