from .models import Fund

def add_tickers_to_context(request):

    tickers_list = [f.ticker for f in Fund.objects.all()]
    return {
        "tickers_list": tickers_list
    }