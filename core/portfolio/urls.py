from django.urls import path
from portfolio.views import *

app_name  = 'portfolio'

urlpatterns = [
    path('' , portfolio_view, name='index'),
    path('<int:pid>', portfolio_single_view, name='single'),
]
