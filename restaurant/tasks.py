import csv
from io import StringIO

from celery import shared_task

from restaurant import pastebin, models


@shared_task
def create_paste():
    fields = ["name", "price", "price_currency"]
    dishes = models.Dish.objects.values(*fields)
    with StringIO() as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(dishes)
        code = f.getvalue()
        return pastebin.create_paste(code)
