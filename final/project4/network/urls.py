
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    # path('newpost', views.new_post),
    # path('u/<username>', views.profile, name="profile"),
    # path('following/', views.following, name="following"),
    # path('follow/', views.follow),
    # path('edit_post/', views.edit_post),
    # path('like/', views.like),

]
