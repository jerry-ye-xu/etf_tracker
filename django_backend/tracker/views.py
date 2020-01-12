from django.shortcuts import render

# Create your views here.

from django.views.generic import (
    ListView,
    DetailView
)

from .models import Fund, FundPrices

class FundListView(ListView):
    model = Fund
    context_object_name = "funds_list"
    template_name = "tracker/_pages/home.html"
    # paginate_by = 5