from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.views.decorators.http import require_GET, require_POST
from django.views.generic import FormView, TemplateView

from restaurant import forms


class IndexView(FormView):
    template_name = "restaurant/index.html"
    form_class = forms.IndexForm
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

    def get_context_data(self, **kwargs):
        kwargs["create_dish_form"] = forms.CreateDishForm(prefix="create_dish")
        return super().get_context_data(**kwargs)


index = require_GET(IndexView.as_view())
order = require_POST(IndexView.as_view())


class CreatePasteView(TemplateView):
    template_name = "restaurant/paste.html"
