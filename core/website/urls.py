from django.urls import path, include
from .views import (
    IndexView,
    AboutView,
    PortfolioView,
    ContactView,
)

app_name = "website"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("about/", AboutView.as_view(), name="about"),
    path("portfolio/", PortfolioView.as_view(), name="portfolio"),
    path("contact/", ContactView.as_view(), name="contact"),

    path("api/v1/", include("todo.api.v1.urls")),
]