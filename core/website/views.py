from django.shortcuts import redirect, render
from django.views.generic import (
    View,
    ListView,
    CreateView,
)
from core.celery import delete_rejected_comments
from django.urls import reverse_lazy
from .models import Skill, Portfolio, Contact
from accounts.models import Profile
from .forms import CreateContactForm
from blog.models import Post

# Create your views here.

class IndexView(ListView):
    model = Skill
    template_name = 'index/index.html'
    context_object_name = "skills"
    # delete_rejected_comments.delay()

    def get_queryset(self):
        # return all the Skill objects
        return self.model.objects.all()

class AboutView(ListView):
    model = Profile
    template_name = 'index/sections/about.html'
    context_object_name = "profile"

    def get_queryset(self):
        # return all the Skill objects
        return self.model.objects.get(user__email="admin@admin.com")

class PortfolioView(ListView):
    model = Portfolio
    template_name = 'index/sections/portfolio.html'
    context_object_name = "works"
    
    def get_queryset(self):
        # return 6 last works
        return self.model.objects.all().order_by('-created_date')[:6]

class BlogView(ListView):
    model = Post
    template_name = 'index/sections/blog-latest.html'
    context_object_name = "posts"

    def get_queryset(self):
        # return 6 last posts
        return self.model.objects.all().order_by('-created_date')[:6]
 
class ContactView(CreateView):
    model = Contact
    form_class = CreateContactForm
    success_url = reverse_lazy("website:index")
    template_name = "index/sections/contact.html"