import datetime as dt

from django.shortcuts import render

# Create your views here.

from django.views.generic import (
    ListView,
    DetailView
)

from .models import Fund, FundPrices

DATE_FORMAT = "%Y-%m-%d"

def filter_dates(n):
    return dt.datetime.today() - dt.timedelta(days=n)

class FundListView(ListView):
    model = Fund
    context_object_name = "funds_list"
    template_name = "tracker/_pages/home.html"
    # paginate_by = 5

    ordering = ["-most_recent_date"]

    def get_context_data(self, *args, **kwargs):
        cutoff_date = filter_dates(n=10)

        context = super(FundListView, self).get_context_data(**kwargs)
        context["funds_prices"] = FundPrices.objects.filter(date__gte=cutoff_date)

        print(context["funds_prices"])

        return context