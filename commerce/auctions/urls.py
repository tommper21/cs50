from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("create/", views.create, name="create"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("<str:listing_title>", views.listing, name="listing"),
    path("<str:listing_title>/bid/", views.bid, name="bid"),
    path("<str:listing_title>/close/", views.close, name="close"),
    path("<str:listing_title>/comment/", views.comment, name="comment"),
    path("category/", views.category, name="category"),
    path("category/<str:category>", views.category_listing, name="category_listing")

]
