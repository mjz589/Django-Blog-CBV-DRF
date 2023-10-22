from django.urls import path
from .views import (
    IndexView,
    ContactView,
)

app_name = "website"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("contact", ContactView.as_view(), name="contact"),
]
