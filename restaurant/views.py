from celery.result import AsyncResult
from django.http import JsonResponse
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.decorators.http import require_GET, require_POST
from django.views.generic import FormView

from restaurant import tasks
from restaurant.forms import IndexForm


class IndexView(FormView):
    template_name = "restaurant/index.html"
    form_class = IndexForm
    success_url = reverse_lazy("restaurant:index")

    def form_valid(self, form):
        dishes = form.cleaned_data["dishes"]
        total_price = sum(dish.price for dish in dishes)
        allergens = {
            allergen
            for dish in dishes.prefetch_related("allergens")
            for allergen in dish.allergens.all()
        }
        return TemplateResponse(self.request, "restaurant/order.html", context={
            "total_price": total_price,
            "dishes": dishes,
            "allergens": allergens
        })


index = require_GET(IndexView.as_view())
order = require_POST(IndexView.as_view())


class CreatePasteView(View):
    def get(self, request):
        task_id = request.GET["task_id"]
        res = AsyncResult(task_id)
        data = {
            "id": task_id,
            "status": res.status,
            "result": str(res.result),
        }
        print(data)
        return JsonResponse(data)

    def post(self, request):
        res = tasks.create_paste.delay("foo bar qwe")
        return TemplateResponse(request, "restaurant/paste.html", context={
            "task_id": res.id
        })
        # return JsonResponse({
        #     "id": res.id
        # })
