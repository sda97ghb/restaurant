"""restaurant app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from restaurant import views
    2. Add a URL to urlpatterns:  path("", views.home, name="home")
Class-based views
    1. Add an import:  from restaurant import views
    2. Add a URL to urlpatterns:  path("", views.Home.as_view(), name="home")
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path("blog/", include("blog.urls"))
"""
from django.urls import path

from restaurant import views

app_name = "restaurant"

urlpatterns = [
    path("", views.index, name="index"),
    path("order/", views.order, name="order"),
    path("pastebin/", views.CreatePasteView.as_view(), name="pastebin")
]
