from .serializers import PortfolioSerializer
from ...models import Portfolio
from .permissions import IsAdminOrReadOnly

# or instead of ...models you can point models.py like this: todo.models

# class-based views for api
from rest_framework import viewsets

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .paginations import DefaultPagination

# caching
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers  # vary_on_cookie,


class WorkModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = PortfolioSerializer
    # filters
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = [
        "category",
    ]
    search_fields = [
        "title",
        "client",
        "project_url",
    ]
    ordering_fields = ["created_date"]
    # pagination
    pagination_class = DefaultPagination

    # caching
    @method_decorator(cache_page(60 * 10))
    @method_decorator(vary_on_headers("Authorization",))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        # define the queryset wanted
        works = Portfolio.objects.all()
        return works
