from django.urls import path

from restaurant.api import views

app_name = "restaurant_api"

urlpatterns = [
    path("pastebin/tasks/", views.CreatePastebinTaskView.as_view(), name="pastebin_task_create"),
    path("pastebin/tasks/<str:task_id>/", views.PastebinTaskView.as_view(), name="pastebin_task_status"),
]
