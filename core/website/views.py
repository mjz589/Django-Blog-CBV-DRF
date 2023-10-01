from django.shortcuts import redirect, render
from django.views.generic import (
    View,
    ListView,
)

from django.urls import reverse_lazy
from .models import Skill, Portfolio
from accounts.models import Profile
from core.celery import delete_rejected_comments
from datetime import datetime

# Create your views here.

class IndexView(ListView):
    model = Skill
    template_name = 'index.html'
    context_object_name = "skills"
    delete_rejected_comments.delay()

    def get_queryset(self):
        # return all the Skill objects
        return self.model.objects.all()

class AboutView(ListView):
    model = Profile
    template_name = 'index.html'
    context_object_name = "profile"

    def get_queryset(self):
        # return all the Skill objects
        return self.model.objects.get(user__email="admin@admin.com")

class PortfolioView(ListView):
    model = Portfolio
    template_name = 'index.html'
    context_object_name = "work"

    def get_queryset(self):
        # return all the Skill objects
        return self.model.objects.filter(created_date__gt=datetime.now())

class ContactView(ListView):
    model = Skill
    template_name = 'index.html'
    context_object_name = "skills"

    def get_queryset(self):
        # return all the Skill objects
        return self.model.objects.all()