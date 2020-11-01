import re

from django.http import QueryDict
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer

from restaurant import models


class DishSerializer(ModelSerializer):
    class Meta:
        model = models.Dish
        fields = ["id", "name", "nutritional_value", "price", "price_currency", "image", "category", "allergens"]
        extra_kwargs = {
            "price": {
                "required": True
            },
        }

    allergens = PrimaryKeyRelatedField(many=True, queryset=models.Allergen.objects.all(), required=False)

    def patch_allergens(self, data):
        # multipart/form-data sends allergens like "1,2,3" which will be parsed as ["1,2,3"] and will cause
        # ValidationError. Solution: Manually convert it to [1, 2, 3].
        if isinstance(data, QueryDict):
            if "allergens" in data:
                data = data.copy()  # data can be an immutable QueryDict
                allergens = data.getlist("allergens")
                if len(allergens) == 1 and type(allergens[0]) == str:
                    if re.match(r"[0-9]+(,[0-9]+)*", allergens[0]):
                        allergens = list(map(int, data["allergens"].split(",")))
                    elif len(allergens[0]) == 0:
                        allergens = []
                    data.setlist("allergens", allergens)
        return data

    def to_internal_value(self, data):
        data = self.patch_allergens(data)
        return super().to_internal_value(data)

    def create(self, validated_data):
        allergens = validated_data.pop("allergens", [])
        dish = super().create(validated_data)
        if allergens:
            dish.allergens.set(allergens)
        return dish
