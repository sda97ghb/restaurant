from celery.result import AsyncResult
from rest_framework.generics import get_object_or_404, RetrieveAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from restaurant import tasks, models
from restaurant.api import parsers
from restaurant.api import serializers


class CreatePastebinTaskView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        res = tasks.create_paste.delay()
        return Response(res.id)


class PastebinTaskView(APIView):
    authentication_classes = []
    permission_classes = []

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
