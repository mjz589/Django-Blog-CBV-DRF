from django.shortcuts import render,get_object_or_404 , HttpResponseRedirect, redirect

from django.utils import timezone
from .models import *
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from blog.forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.generic import (
    View,
    ListView,
    DetailView,
)

# Create your views here.

def portfolio_view(request, *args, **kwargs):
    portfolio = Portfolio.objects.all()
    
    # pagination
    portfolio = Paginator(portfolio, 3)
    try :
        page_number = request.GET.get('page')
        portfolio = portfolio.get_page(page_number)
    except PageNotAnInteger:
        portfolio = portfolio.get_page(1)
    except EmptyPage:
        portfolio = portfolio.get_page(1)

    context={'portfolio': portfolio}
    return render(request, 'Portfolio/Portfolio.html', context)



# def portfolio_single_view(request, pid):
#     Portfolio = get_object_or_404(Portfolio, pk=pid , published_date__lte=timezone.now())
#     related_portfolio = Portfolio.objects.filter(type=Portfolio.type)
#     context = {'Portfolio': Portfolio , 'related_portfolio':related_portfolio , }
#     return render(request, 'Portfolio/Portfolio_details.html', context)

class PortfolioDetail(DetailView):
    model = Portfolio
    template_name = "portfolio/portfolio-details.html"
    context_object_name = "work"