from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("<str:name>", views.page, name="page"),
    path("search/", views.search, name="search"),
    path("create/", views.create, name="create"),
    path("rand/", views.rand, name="rand"),
    path("wiki/<str:name>", views.page, name="wiki"),
    path("edit/<str:name>", views.edit, name="edit")
]
