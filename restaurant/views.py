from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.views import View

from restaurant.forms import IndexForm


class IndexView(View):
    def get(self, request):
        form = IndexForm()
        return TemplateResponse(request, "restaurant/index.html", context={
            "form": form
        })

    def post(self, request):
        form = IndexForm(request.POST)
        return HttpResponseRedirect(reverse("restaurant:index"))
