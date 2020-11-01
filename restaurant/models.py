from django.db import models
from djmoney.models.fields import MoneyField
from django.utils.translation import gettext_lazy as _


class Allergen(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    class Meta:
        verbose_name = _("Allergen")
        verbose_name_plural = _("Allergens")
    
    def __str__(self):
        return self.name


class DishCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    class Meta:
        verbose_name = _("Dish category")
        verbose_name_plural = _("Dish categories")

    def __str__(self):
        return self.name


class Dish(models.Model):
    name = models.CharField(max_length=100)
    nutritional_value = models.IntegerField()
    price = MoneyField(max_digits=10, decimal_places=2, default_currency="RUB")
    image = models.ImageField(upload_to="restaurant/dish_image/", blank=True)
    allergens = models.ManyToManyField(Allergen, blank=True)
    category = models.ForeignKey(DishCategory, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = _("Dish")
        verbose_name_plural = _("Dishes")
        unique_together = ["name", "category"]

    def __str__(self):
        return f"{self.name}, {self.category}, {self.price}"
