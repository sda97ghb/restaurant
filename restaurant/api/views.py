from celery.result import AsyncResult
from rest_framework.response import Response
from rest_framework.views import APIView

from restaurant import tasks


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
