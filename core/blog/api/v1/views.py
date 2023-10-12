from rest_framework.response import Response
from .serializers import TaskSerializer
from ...models import Task
from .permissions import IsOwnerOrReadOnly
# or instead of ...models you can point models.py like this: todo.models
from accounts.models import Profile

# class-based views for api
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers


from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .paginations import DefaultPagination

# caching
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers  # vary_on_cookie,
import requests
from decouple import config


class TaskModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = TaskSerializer
    # filters
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = [
        "category", "tags",
    ]
    search_fields = [
        "title", "summary", "content",
    ]
    ordering_fields = ["published_date"]
    # pagination
    pagination_class = DefaultPagination

    """ --- we used another method for user providing ---
    def perform_create(self, serializer):
        # user must automatically be provided and not be written by users
        profile = Profile.objects.get(user=self.request.user.id)
        serializer.save(user=profile) """

    def get_queryset(self):
        # define the queryset wanted
        if self.request.user.is_verified:
            profile = Profile.objects.get(user=self.request.user.id)
            queryset = Task.objects.filter(user=profile.id)
        else:
            raise serializers.ValidationError(
                {"detail": "User is not verified."}
            )
        return queryset

    # extra actions
    @action(
        methods=[
            "GET",
        ],
        detail=False,
    )
    def get_ok(self, request):
        return Response({"detail": "extra actions -OK-"})

