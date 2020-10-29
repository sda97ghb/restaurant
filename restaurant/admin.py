from django.contrib import admin
from restaurant import models


class DishAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "nutritional_value")
    list_filter = ("category",)


admin.site.register(models.Allergen)
admin.site.register(models.DishCategory)
admin.site.register(models.Dish, DishAdmin)
