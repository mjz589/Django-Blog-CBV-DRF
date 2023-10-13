from rest_framework.routers import DefaultRouter
from . import views

app_name = "api-v1"

router = DefaultRouter()
router.register("work", views.WorkModelViewSet, basename="work")
urlpatterns = router.urls
