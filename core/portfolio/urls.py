from django.urls import path, include
from portfolio.views import *

app_name  = 'portfolio'

urlpatterns = [
    path('' , portfolio_view, name='index'),
    path('<int:pk>', PortfolioDetail.as_view(), name='detail'),
    path("api/v1/", include("portfolio.api.v1.urls")),
]
