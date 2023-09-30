from django.shortcuts import redirect, render
from django.views.generic import (
    View,
    ListView,
)

from django.urls import reverse_lazy
from .models import Skill
from accounts.models import Profile
from core.celery import delete_completed_tasks

# Create your views here.

class IndexView(ListView):
    