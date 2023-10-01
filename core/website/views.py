from django.shortcuts import redirect, render
from django.views.generic import (
    View,
    ListView,
)

from django.urls import reverse_lazy
from .models import Skill
from accounts.models import Profile
# from core.celery import delete_rejected_comments

# Create your views here.

class IndexView(ListView):
    model = Skill
    template_name = 'index.html'
    context_object_name = "skills"
    # delete_rejected_comments.delay()

    def get_queryset(self):
        # return all the Skill objects
        return self.model.objects.all()

class AboutView(ListView):
    model = Skill
    template_name = 'index.html'
    context_object_name = "skills"
    # delete_rejected_comments.delay()

    def get_queryset(self):
        # return all the Skill objects
        return self.model.objects.all()

class PortfolioView(ListView):
    model = Skill
    template_name = 'index.html'
    context_object_name = "skills"
    # delete_rejected_comments.delay()

    def get_queryset(self):
        # return all the Skill objects
        return self.model.objects.all()

class ContactView(ListView):
    model = Skill
    template_name = 'index.html'
    context_object_name = "skills"
    # delete_rejected_comments.delay()

    def get_queryset(self):
        # return all the Skill objects
        return self.model.objects.all()