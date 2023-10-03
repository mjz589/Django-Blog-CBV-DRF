from django.urls import path
from portfolio.views import *

app_name  = 'portfolio'

urlpatterns = [
    path('' , portfolio_view, name='index'),
    path('<int:pk>', PortfolioDetail.as_view(), name='detail'),
]
