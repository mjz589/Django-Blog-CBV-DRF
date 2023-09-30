from django.urls import path, include
from .views import (
    TaskList,
    About,
    Portfolio,
    Contact,
)

app_name = "website"

urlpatterns = [
    path("", TaskList.as_view(), name="task_list"),
    path("", About.as_view(), name="about"),
    path("", Portfolio.as_view(), name="portfolio"),
    path("", Contact.as_view(), name="contact"),

    path("api/v1/", include("todo.api.v1.urls")),
]