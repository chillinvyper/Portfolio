"""
URL configuration for sticky_notes project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import (
    note_list,
    note_detail,
    note_create,
    note_update,
    note_delete,
)

urlpatterns = [
    # url pattern for displaying a list of all note
    path("", note_list, name="note_list"),

    # url pattern for displaying details of a specific note
    path("note/<int:pk>/", note_detail, name="note_detail"),

    # url pattern for creating a note
    path("note/new/", note_create, name="note_create"),

    # url pattern for updating an existing note
    path("note/<int:pk>/edit/", note_update, name="note_update"),

    # url pattern for deleting an existing note
    path("post/<int:pk>/delete/", note_delete, name="note_delete"),
]
