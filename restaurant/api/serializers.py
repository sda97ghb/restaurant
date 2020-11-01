from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer

from restaurant import models


class DishSerializer(ModelSerializer):
    class Meta:
        model = models.Dish
        fields = ["id", "name", "nutritional_value", "price", "price_currency", "image", "category", "allergens"]

    allergens = PrimaryKeyRelatedField(many=True, queryset=models.Allergen.objects.all(), required=False)

    def create(self, validated_data):
        allergens = validated_data.pop("allergens", [])
        dish = super().create(validated_data)
        if allergens:
            dish.allergens.set(allergens)
        return dish
