from django.urls import path, include
from .views import FundListView

urlpatterns = [
    path('', FundListView.as_view(), name='tracker-home')
]
