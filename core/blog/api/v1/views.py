from django.utils import timezone
from rest_framework.response import Response

# local
from .serializers import PostSerializer
from ...models import Post
from .permissions import IsAdminOrReadOnly
from .filters import PostFilter

# class-based views for api
from rest_framework import viewsets
from rest_framework.decorators import action

# filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

# pagination
from .paginations import DefaultPagination

# caching
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers  # vary_on_cookie,


class PostModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = PostSerializer
    # filters
    filter_class = PostFilter
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # filterset_fields = [
    #     "category", "tags",
    # ]
    search_fields = [
        "title",
        "summary",
        "content",
    ]
    ordering_fields = ["published_date"]
    # pagination
    pagination_class = DefaultPagination

    # caching
    @method_decorator(cache_page(60 * 10))
    @method_decorator(
        vary_on_headers(
            "Authorization",
        )
    )
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        # define the queryset wanted
        posts = Post.objects.filter(published_date__lte=timezone.now()).order_by(
            "-published_date"
        )
        return posts

    # extra actions
    @action(
        methods=[
            "GET",
        ],
        detail=False,
    )
    def get_ok(self, request):
        return Response({"detail": "extra actions -OK-"})
