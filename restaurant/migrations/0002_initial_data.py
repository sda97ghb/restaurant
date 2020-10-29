from django.db import migrations, transaction
from djmoney.money import Money


def populate_data(apps, schema_editor):
    Allergen = apps.get_model("restaurant", "Allergen")
    DishCategory = apps.get_model("restaurant", "DishCategory")
    Dish = apps.get_model("restaurant", "Dish")

    db_alias = schema_editor.connection.alias

    with transaction.atomic():
        gluten = Allergen.objects.using(db_alias).create(name="Cereals containing gluten")
        crustaceans = Allergen.objects.using(db_alias).create(name="Crustaceans")
        egg = Allergen.objects.using(db_alias).create(name="Egg")
        fish = Allergen.objects.using(db_alias).create(name="Fish")
        soybeans = Allergen.objects.using(db_alias).create(name="Soybeans")
        milk = Allergen.objects.using(db_alias).create(name="Milk (including lactose)")
        mustard = Allergen.objects.using(db_alias).create(name="Mustard")
        sulphur = Allergen.objects.using(db_alias).create(name="Sulphur dioxide and sulphites")
        mollusks = Allergen.objects.using(db_alias).create(name="Mollusks")

        cold_starters = DishCategory.objects.using(db_alias).create(name="Cold starters")
        salads = DishCategory.objects.using(db_alias).create(name="Salads")
        bruschettas = DishCategory.objects.using(db_alias).create(name="Bruschettas")
        folded_calzone_pizzas = DishCategory.objects.using(db_alias).create(name="Folded calzone pizzas")
        special_pizzas = DishCategory.objects.using(db_alias).create(name="Special pizzas")
        red_pizzas = DishCategory.objects.using(db_alias).create(name="Red pizzas")
        pizzas_with_chili = DishCategory.objects.using(db_alias).create(name="Pizzas with chili")
        lactose_free_pizzas = DishCategory.objects.using(db_alias).create(name="Lactose-free pizzas")
        white_pizzas = DishCategory.objects.using(db_alias).create(name="White pizzas")
        focaccias = DishCategory.objects.using(db_alias).create(name="Focaccias")

        Dish.objects.using(db_alias).create(name="Potato croquettes and mozzarella", nutritional_value=1, price=Money(1.30, "EUR"), category=cold_starters).allergens.add(gluten, egg, milk)
        Dish.objects.using(db_alias).create(name="Mini buffalo mozzarella", nutritional_value=1, price=Money(3.50, "EUR"), category=cold_starters).allergens.add(gluten, milk)
        Dish.objects.using(db_alias).create(name="Ascolana-style olives", nutritional_value=1, price=Money(3.50, "EUR"), category=cold_starters).allergens.add(gluten, egg)
        Dish.objects.using(db_alias).create(name="Squash blossom", nutritional_value=1, price=Money(2.50, "EUR"), category=cold_starters).allergens.add(gluten, egg, fish)
        Dish.objects.using(db_alias).create(name="Fillet of cod", nutritional_value=1, price=Money(2.50, "EUR"), category=cold_starters).allergens.add(fish)

        Dish.objects.using(db_alias).create(name="Chicory", nutritional_value=1, price=Money(9.00, "EUR"), category=salads).allergens.add(gluten, milk)
        Dish.objects.using(db_alias).create(name="Mexican", nutritional_value=1, price=Money(9.00, "EUR"), category=salads).allergens.add(gluten)
        Dish.objects.using(db_alias).create(name="Summer", nutritional_value=1, price=Money(10.50, "EUR"), category=salads).allergens.add(gluten, milk)
        Dish.objects.using(db_alias).create(name="Spring", nutritional_value=1, price=Money(10.00, "EUR"), category=salads).allergens.add(gluten, fish)
        Dish.objects.using(db_alias).create(name="Pink shrimp", nutritional_value=1, price=Money(9.50, "EUR"), category=salads).allergens.add(gluten, crustaceans, soybeans, mustard)

        Dish.objects.using(db_alias).create(name="Tomatoes and basil", nutritional_value=1, price=Money(1.50, "EUR"), category=bruschettas).allergens.add(gluten)
        Dish.objects.using(db_alias).create(name="Mushrooms and mozzarella", nutritional_value=1, price=Money(2.00, "EUR"), category=bruschettas).allergens.add(gluten, milk)
        Dish.objects.using(db_alias).create(name="Anchovies and mozzarella", nutritional_value=1, price=Money(2.00, "EUR"), category=bruschettas).allergens.add(gluten, fish, milk)
        Dish.objects.using(db_alias).create(name="Cooked ham and mozzarella", nutritional_value=1, price=Money(2.00, "EUR"), category=bruschettas).allergens.add(gluten, milk)
        Dish.objects.using(db_alias).create(name="Mozzarella with pancetta and black pepper", nutritional_value=1, price=Money(2.00, "EUR"), category=bruschettas).allergens.add(gluten, milk)
        Dish.objects.using(db_alias).create(name="Mozzarella and raw ham", nutritional_value=1, price=Money(2.00, "EUR"), category=bruschettas).allergens.add(gluten, milk)

        Dish.objects.using(db_alias).create(name="Cooked ham and mozzarella", nutritional_value=1, price=Money(9.00, "EUR"), category=folded_calzone_pizzas).allergens.add(gluten, milk)
        Dish.objects.using(db_alias).create(name="Raw ham and mozzarella", nutritional_value=1, price=Money(9.00, "EUR"), category=folded_calzone_pizzas).allergens.add(gluten, milk)
        Dish.objects.using(db_alias).create(name="Mushrooms and \"salsiccia\" sausages", nutritional_value=1, price=Money(9.00, "EUR"), category=folded_calzone_pizzas).allergens.add(gluten)
        Dish.objects.using(db_alias).create(name="Spicy sausage and mozzarella", nutritional_value=1, price=Money(9.00, "EUR"), category=folded_calzone_pizzas).allergens.add(gluten, milk)
        Dish.objects.using(db_alias).create(name="Broccoli, sausage and mozzarella", nutritional_value=1, price=Money(9.00, "EUR"), category=folded_calzone_pizzas).allergens.add(gluten, milk)
        Dish.objects.using(db_alias).create(name="Roman", nutritional_value=1, price=Money(9.00, "EUR"), category=folded_calzone_pizzas).allergens.add(gluten, milk)

        Dish.objects.using(db_alias).create(name="Yellow pumpkin", nutritional_value=1, price=Money(10.00, "EUR"), category=special_pizzas).allergens.add(gluten, milk)
        Dish.objects.using(db_alias).create(name="The devil's belly button", nutritional_value=1, price=Money(10.00, "EUR"), category=special_pizzas).allergens.add(gluten)
        Dish.objects.using(db_alias).create(name="A Bona", nutritional_value=1, price=Money(10.00, "EUR"), category=special_pizzas).allergens.add(gluten, milk)
        Dish.objects.using(db_alias).create(name="Roberto", nutritional_value=1, price=Money(9.50, "EUR"), category=special_pizzas).allergens.add(gluten, milk)
        Dish.objects.using(db_alias).create(name="Ruby", nutritional_value=1, price=Money(9.00, "EUR"), category=special_pizzas).allergens.add(egg, milk)
        Dish.objects.using(db_alias).create(name="Gabriel", nutritional_value=1, price=Money(10.00, "EUR"), category=special_pizzas).allergens.add(gluten, milk)
        Dish.objects.using(db_alias).create(name="Crudo in bocca", nutritional_value=1, price=Money(10.00, "EUR"), category=special_pizzas).allergens.add(gluten, milk)
        Dish.objects.using(db_alias).create(name="Seafood", nutritional_value=1, price=Money(12.00, "EUR"), category=special_pizzas).allergens.add(crustaceans, mollusks)

        Dish.objects.using(db_alias).create(name="Contadina", nutritional_value=1, price=Money(9.00, "EUR"), category=red_pizzas).allergens.add(gluten, milk)
        Dish.objects.using(db_alias).create(name="Vienna", nutritional_value=1, price=Money(6.50, "EUR"), category=red_pizzas).allergens.add(gluten, milk)
        Dish.objects.using(db_alias).create(name="Funghi rossa", nutritional_value=1, price=Money(6.50, "EUR"), category=red_pizzas).allergens.add(gluten, milk)
        Dish.objects.using(db_alias).create(name="Boscaiola rossa", nutritional_value=1, price=Money(7.50, "EUR"), category=red_pizzas).allergens.add(gluten, milk)
        Dish.objects.using(db_alias).create(name="Capricciosa", nutritional_value=1, price=Money(8.00, "EUR"), category=red_pizzas).allergens.add(gluten, egg, milk)
        Dish.objects.using(db_alias).create(name="Salsiccia", nutritional_value=1, price=Money(6.50, "EUR"), category=red_pizzas).allergens.add(gluten, milk)
        Dish.objects.using(db_alias).create(name="Margherita", nutritional_value=1, price=Money(6.00, "EUR"), category=red_pizzas).allergens.add(gluten, milk)
        Dish.objects.using(db_alias).create(name="Napoli", nutritional_value=1, price=Money(6.50, "EUR"), category=red_pizzas).allergens.add(gluten, milk)
        Dish.objects.using(db_alias).create(name="Parmigiana", nutritional_value=1, price=Money(10.00, "EUR"), category=red_pizzas).allergens.add(gluten, milk)

        Dish.objects.using(db_alias).create(name="Diavola", nutritional_value=1, price=Money(7.00, "EUR"), category=pizzas_with_chili).allergens.add(gluten, milk)
        Dish.objects.using(db_alias).create(name="May fire", nutritional_value=1, price=Money(8.50, "EUR"), category=pizzas_with_chili).allergens.add(gluten, milk)
        Dish.objects.using(db_alias).create(name="Calabrian", nutritional_value=1, price=Money(9.00, "EUR"), category=pizzas_with_chili).allergens.add(gluten, milk)
        Dish.objects.using(db_alias).create(name="Diavolessa", nutritional_value=1, price=Money(10.00, "EUR"), category=pizzas_with_chili).allergens.add(gluten, milk)
        Dish.objects.using(db_alias).create(name="Temptation of the devil", nutritional_value=1, price=Money(10.00, "EUR"), category=pizzas_with_chili).allergens.add(gluten, milk)
        Dish.objects.using(db_alias).create(name="Amatriciana", nutritional_value=1, price=Money(8.00, "EUR"), category=pizzas_with_chili).allergens.add(gluten, milk, sulphur)

        Dish.objects.using(db_alias).create(name="Rossa San Daniele", nutritional_value=1, price=Money(6.50, "EUR"), category=lactose_free_pizzas).allergens.add(gluten)
        Dish.objects.using(db_alias).create(name="Trentina", nutritional_value=1, price=Money(7.50, "EUR"), category=lactose_free_pizzas).allergens.add(gluten)
        Dish.objects.using(db_alias).create(name="Rossa", nutritional_value=1, price=Money(4.50, "EUR"), category=lactose_free_pizzas).allergens.add(gluten)
        Dish.objects.using(db_alias).create(name="Rossa special", nutritional_value=1, price=Money(6.50, "EUR"), category=lactose_free_pizzas).allergens.add(gluten)
        Dish.objects.using(db_alias).create(name="The devil's shadow", nutritional_value=1, price=Money(10.00, "EUR"), category=lactose_free_pizzas).allergens.add(gluten)

        Dish.objects.using(db_alias).create(name="Berlino", nutritional_value=1, price=Money(7.50, "EUR"), category=white_pizzas).allergens.add(gluten, milk)
        Dish.objects.using(db_alias).create(name="Milano", nutritional_value=1, price=Money(8.00, "EUR"), category=white_pizzas).allergens.add(gluten, milk)
        Dish.objects.using(db_alias).create(name="Tedesca", nutritional_value=1, price=Money(7.00, "EUR"), category=white_pizzas).allergens.add(gluten, milk)
        Dish.objects.using(db_alias).create(name="Crayfish", nutritional_value=1, price=Money(8.00, "EUR"), category=white_pizzas).allergens.add(gluten, crustaceans, milk)

        Dish.objects.using(db_alias).create(name="Rosemary", nutritional_value=1, price=Money(4.00, "EUR"), category=focaccias).allergens.add()
        Dish.objects.using(db_alias).create(name="Trento", nutritional_value=1, price=Money(8.50, "EUR"), category=focaccias).allergens.add(gluten, milk)
        Dish.objects.using(db_alias).create(name="Carpaccio", nutritional_value=1, price=Money(9.50, "EUR"), category=focaccias).allergens.add(milk)
        Dish.objects.using(db_alias).create(name="Caprese", nutritional_value=1, price=Money(9.50, "EUR"), category=focaccias).allergens.add(gluten, milk)
        Dish.objects.using(db_alias).create(name="Bufala", nutritional_value=1, price=Money(9.50, "EUR"), category=focaccias).allergens.add(gluten, milk)
        Dish.objects.using(db_alias).create(name="Rocket salad", nutritional_value=1, price=Money(8.00, "EUR"), category=focaccias).allergens.add()
        Dish.objects.using(db_alias).create(name="Gamberetto", nutritional_value=1, price=Money(9.00, "EUR"), category=focaccias).allergens.add(gluten, crustaceans, soybeans, mustard)
        Dish.objects.using(db_alias).create(name="Tonnarello", nutritional_value=1, price=Money(9.50, "EUR"), category=focaccias).allergens.add(gluten, fish)


class Migration(migrations.Migration):
    dependencies = [
        ("restaurant", "0001_initial")
    ]

    operations = [
        migrations.RunPython(populate_data)
    ]
