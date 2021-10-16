
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("<str:profile>", views.profile, name="profile"),
    path("<str:profile>/follow", views.follow, name="follow"),
    path("posts/<int:post_id>", views.post, name="post"),
    path("likes/<int:post_id>", views.like, name="like")
]
