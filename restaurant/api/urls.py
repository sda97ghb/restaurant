from django.urls import path

from restaurant.api import views

app_name = "restaurant_api"

urlpatterns = [
    path("pastebin/tasks/", views.CreatePastebinTaskView.as_view(), name="pastebin_task_create"),
    path("pastebin/tasks/<str:task_id>/", views.PastebinTaskView.as_view(), name="pastebin_task_status"),
    path("dishes/", views.ListCreateDishView.as_view(), name="dishes"),
    path("dishes/<int:pk>/", views.DishView.as_view(), name="dish_details"),
    path("dishes/<int:pk>/image/", views.UpdateDishImageView.as_view(), name="update_dish_image"),
]
