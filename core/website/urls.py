from django.urls import path, include
from .views import (
    IndexView,
    AboutView,
    PortfolioView,
    ContactView,
    BlogView,
)

app_name = "website"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("about/", AboutView.as_view(), name="about"),
    path("portfolio/", PortfolioView.as_view(), name="portfolio"),
    path("contact/", ContactView.as_view(), name="contact"),
    path('blog/', BlogView.as_view(), name='blog'),

    # path("api/v1/", include("website.api.v1.urls")),
]