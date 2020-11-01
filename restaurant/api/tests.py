import json

from django.conf import settings
from django.test import TestCase, Client
from djmoney.money import Money
from rest_framework.reverse import reverse

from restaurant import models


class CreateDishTests(TestCase):
    minimal_valid_input = {
        "name": "foo",
        "nutritional_value": 120,
        "price": "12.70",
        "category": 1
    }
    minimal_expected_output_without_id = {
        "name": "foo",
        "nutritional_value": 120,
        "price": "12.70",
        "price_currency": "RUB",
        "category": 1,
        "image": None,
        "allergens": []
    }

    def check_created_dish(self, pk):
        dish = models.Dish.objects.get(pk=pk)
        self.assertEqual(dish.name, self.minimal_expected_output_without_id["name"])
        self.assertEqual(dish.nutritional_value, self.minimal_expected_output_without_id["nutritional_value"])
        self.assertEqual(dish.price, Money(amount=self.minimal_expected_output_without_id["price"],
                                           currency=self.minimal_expected_output_without_id["price_currency"]))
        self.assertEqual(dish.category.id, self.minimal_expected_output_without_id["category"])
        if self.minimal_expected_output_without_id["image"] is None:
            self.assertFalse(dish.image)
        else:
            self.assertEqual(dish.image, self.minimal_expected_output_without_id["image"])
        self.assertEqual(dish.allergens.count(), len(self.minimal_expected_output_without_id["allergens"]))

    def test_good_case_json(self):
        c = Client()

        response = c.post(
            reverse("restaurant_api:dishes"),
            data=self.minimal_valid_input,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {settings.API_TOKEN}"
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response["Content-Type"], "application/json")

        data = json.loads(response.content)
        self.assertIn("id", data)
        expected = {
            **self.minimal_expected_output_without_id,
            "id": data["id"],
        }
        self.assertEqual(data, expected)

        self.check_created_dish(data["id"])

    def test_json_supports_allergens(self):
        c = Client()

        response = c.post(
            reverse("restaurant_api:dishes"),
            data={
                **self.minimal_valid_input,
                "allergens": [1, 3, 4]
            },
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {settings.API_TOKEN}"
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response["Content-Type"], "application/json")

        data = json.loads(response.content)
        self.assertIn("id", data)
        expected = {
            **self.minimal_expected_output_without_id,
            "id": data["id"],
            "allergens": [1, 3, 4]
        }
        self.assertEqual(data, expected)

        dish = models.Dish.objects.get(pk=data["id"])
        self.assertEqual(list(dish.allergens.values_list("id", flat=True)), expected["allergens"])

    def test_good_case_form_data(self):
        c = Client()

        # content type "multipart/form-data" is used by default
        response = c.post(
            reverse("restaurant_api:dishes"),
            data=self.minimal_valid_input,
            HTTP_AUTHORIZATION=f"Bearer {settings.API_TOKEN}"
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response["Content-Type"], "application/json")

        data = json.loads(response.content)
        self.assertIn("id", data)
        expected = {
            **self.minimal_expected_output_without_id,
            "id": data["id"],
        }
        self.assertEqual(data, expected)

        self.check_created_dish(data["id"])

    def test_form_data_supports_allergens(self):
        c = Client()

        # content type "multipart/form-data" is used by default
        response = c.post(
            reverse("restaurant_api:dishes"),
            data={
                **self.minimal_valid_input,
                "allergens": "1,3,4"
            },
            HTTP_AUTHORIZATION=f"Bearer {settings.API_TOKEN}"
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response["Content-Type"], "application/json")

        data = json.loads(response.content)
        self.assertIn("id", data)
        expected = {
            **self.minimal_expected_output_without_id,
            "id": data["id"],
            "allergens": [1, 3, 4]
        }
        self.assertEqual(data, expected)

        dish = models.Dish.objects.get(pk=data["id"])
        self.assertEqual(list(dish.allergens.values_list("id", flat=True)), expected["allergens"])

    def test_form_data_supports_image(self):
        c = Client()

        with open(settings.BASE_DIR / "restaurant/static/restaurant/img/silhouette.jpg", "rb") as f:
            # content type "multipart/form-data" is used by default
            response = c.post(
                reverse("restaurant_api:dishes"),
                data={
                    **self.minimal_valid_input,
                    "image": f
                },
                HTTP_AUTHORIZATION=f"Bearer {settings.API_TOKEN}"
            )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response["Content-Type"], "application/json")

        data = json.loads(response.content)
        self.assertIn("image", data)
        image_url = data["image"]
        self.assertIsInstance(image_url, str)
        self.assertTrue(image_url.startswith("http"))
        self.assertIn("silhouette", image_url)
        self.assertTrue(image_url.endswith("jpg"))

        dish = models.Dish.objects.get(pk=data["id"])
        self.assertTrue(data["image"].endswith(dish.image.url))

    def test_unauthorized_without_api_token(self):
        c = Client()

        response = c.post(
            reverse("restaurant_api:dishes"),
            data=self.minimal_valid_input,
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 401)

    def test_required_fields(self):
        c = Client()

        for field in self.minimal_valid_input.keys():
            data = self.minimal_valid_input.copy()
            del data[field]

            response = c.post(
                reverse("restaurant_api:dishes"),
                data=data,
                content_type="application/json",
                HTTP_AUTHORIZATION=f"Bearer {settings.API_TOKEN}"
            )
            self.assertEqual(response.status_code, 400)
