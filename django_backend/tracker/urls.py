from django.urls import path, include
from .views import FundListView, FundDetailView, about

urlpatterns = [
    path('', FundListView.as_view(), name='tracker-home'),
    path('fund/<slug:ticker>/', FundDetailView.as_view(), name='tracker-fund-page'),
    path('about/', about, name='tracker-about')
]
