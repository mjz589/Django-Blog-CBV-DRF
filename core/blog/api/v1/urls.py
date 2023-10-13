from rest_framework.routers import DefaultRouter
from django.urls import path
from . import views

app_name = "api-v1"

router = DefaultRouter()
router.register("post", views.PostModelViewSet, basename="post")
urlpatterns = router.urls

"""
from django.urls import path
urlpatterns = [
    # path("task/", views.taskList, name="task-list"),
    path("task/", views.TaskList.as_view(), name="task-list"),
    # path("task/<int:id>/", views.taskDetail, name="task-detail"),
    path("task/<int:pk>/", views.TaskDetail.as_view(), name="task-detail"),
]
urlpatterns += router.urls
"""
