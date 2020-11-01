import re

from celery.result import AsyncResult
from rest_framework.generics import get_object_or_404, RetrieveAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from restaurant import tasks, models
from restaurant.api import parsers
from restaurant.api import serializers


class CreatePastebinTaskView(APIView):
    def post(self, request):
        res = tasks.create_paste.delay()
        return Response(res.id)


class PastebinTaskView(APIView):
    def get(self, request, task_id):
        res = AsyncResult(task_id)
        return Response({
            "id": task_id,
            "status": res.status,
            "result": str(res.result),
        })


class ListCreateDishView(ListCreateAPIView):
    queryset = models.Dish.objects.all()
    serializer_class = serializers.DishSerializer

    def create(self, request, *args, **kwargs):
        # multipart/form-data sends allergens like "1,2,3" which will be parsed as ["1,2,3"] and causes ValidationError.
        # Solution: Manually convert it to [1, 2, 3].
        if "allergens" in request.data:
            allergens = request.data.getlist("allergens")
            if len(allergens) == 1 and type(allergens[0]) == str and re.match(r"[0-9]+(,[0-9]+)*", allergens[0]):
                allergens = list(map(int, request.data["allergens"].split(",")))
                request.data.setlist("allergens", allergens)
        return super().create(request, *args, **kwargs)


class DishView(RetrieveAPIView):
    queryset = models.Dish.objects.all()
    serializer_class = serializers.DishSerializer


class UpdateDishImageView(APIView):
    parser_classes = [parsers.ImageUploadParser]

    def put(self, request, pk):
        dish = get_object_or_404(models.Dish, pk=pk)
        dish.image = request.data["file"]
        dish.save()
        return Response(dish.image.url)

    # Add support for browsers which only accept GET and POST for now.
    def post(self, *args, **kwargs):
        self.put(*args, **kwargs)
