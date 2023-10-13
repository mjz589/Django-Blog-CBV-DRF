from .models import Portfolio
from django.views.generic import (
    DetailView,
)

# Create your views here.


class PortfolioDetail(DetailView):
    model = Portfolio
    template_name = "portfolio/portfolio-details.html"
    context_object_name = "work"


# def portfolio_view(request, *args, **kwargs):
#     portfolio = Portfolio.objects.all()

#     # pagination
#     portfolio = Paginator(portfolio, 3)
#     try:
#         page_number = request.GET.get("page")
#         portfolio = portfolio.get_page(page_number)
#     except PageNotAnInteger:
#         portfolio = portfolio.get_page(1)
#     except EmptyPage:
#         portfolio = portfolio.get_page(1)

#     context = {"portfolio": portfolio}
#     return render(request, "Portfolio/Portfolio.html", context)


# def portfolio_single_view(request, pid):
#     Portfolio = get_object_or_404(Portfolio, pk=pid , published_date__lte=timezone.now())
#     related_portfolio = Portfolio.objects.filter(type=Portfolio.type)
#     context = {'Portfolio': Portfolio , 'related_portfolio':related_portfolio , }
#     return render(request, 'Portfolio/Portfolio_details.html', context)
