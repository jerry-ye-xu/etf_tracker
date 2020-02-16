import datetime as dt
import json
import os

from django.shortcuts import render
from django.core.serializers.json import DjangoJSONEncoder

# Create your views here.

from django.views.generic import (
    ListView,
    DetailView
)

from .models import Fund, FundPrices

DATE_FORMAT = "%Y-%m-%d"

def filter_dates(n):
    return dt.datetime.today() - dt.timedelta(days=n)

def format_json_obj(query_set):
    qset = list(query_set.values_list("fund", "freq_type", "date", "price"))

    d_obj = {}
    for f, ft, d, p in qset:
        # print(f, ft, d, p)
        d_str = d.strftime("%Y-%m-%d")
        if f in d_obj.keys():
            # if len(d_obj) == 0:
            #     d_obj[f] = {ft: {d_str: p}}
            if ("high" not in d_obj[f].keys()):
                d_obj[f][ft] = {d_str: p}
            elif ("low" not in d_obj[f].keys()):
                d_obj[f][ft] = {d_str: p}
            else:
                d_obj[f][ft][d_str] = p
        else:
            d_obj[f] = {ft: {d_str: p}}

    print(d_obj)
    return d_obj

def about(request):

    version = os.environ.get('VERSION')
    context = {
        'version': version
    }

    return render(request, 'tracker/_pages/about.html', context)

class FundListView(ListView):
    model = Fund
    context_object_name = "funds_list"
    template_name = "tracker/_pages/home.html"
    paginate_by = 2

    ordering = ["-most_recent_date"]

    def get_context_data(self, *args, **kwargs):
        context = super(FundListView, self).get_context_data(**kwargs)

        cutoff_date = filter_dates(n=30)
        dict_obj = format_json_obj(FundPrices.objects.filter(date__gte=cutoff_date))

        context["funds_prices"] = json.dumps(dict_obj, cls=DjangoJSONEncoder)

        # print(context["funds_prices"])
        # print(FundPrices.objects.get(date="2019-10-28"))
        # print(context["funds_prices"]["11"]["low"]["2020-01-17"])

        return context

class FundDetailView(DetailView):
    model = Fund
    context_object_name = "fund"
    template_name = "tracker/_pages/fund.html"

    slug_field = "ticker"
    slug_url_kwarg = "ticker"

    def get_context_data(self, *args, **kwargs):
        context = super(FundDetailView, self).get_context_data(**kwargs)

        cutoff_date = filter_dates(n=30)
        dict_obj = format_json_obj(FundPrices.objects.filter(date__gte=cutoff_date))

        context["funds_prices"] = json.dumps(dict_obj, cls=DjangoJSONEncoder)

        # print(context["funds_prices"])

        return context