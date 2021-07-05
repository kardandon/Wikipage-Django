from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("new", views.new, name="new"),
    path("random", views.random, name="random"),
    path("edit/<str:TITLE>", views.edit, name="edit"),
    path("<str:TITLE>", views.title, name="title")
]
