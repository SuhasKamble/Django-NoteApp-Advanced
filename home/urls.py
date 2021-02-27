from django.contrib import admin
from django.urls import path, include
from home import views

urlpatterns = [
    path('', views.Home, name="Home"),
    path("search", views.Search, name="Search"),
    path("createNote", views.createNote, name="createNote"),
    path('delete', views.deleteNote, name="deleteNode"),
    path('edit', views.editNote, name="editNode"),
    path("<str:slug>", views.myNote, name="Note"),
]
