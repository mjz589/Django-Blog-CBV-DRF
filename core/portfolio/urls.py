from django.urls import path, include
from portfolio.views import PortfolioDetail

app_name = "portfolio"

urlpatterns = [
    path("<int:pk>", PortfolioDetail.as_view(), name="detail"),
    path("api/v1/", include("portfolio.api.v1.urls")),
]
