from django.views.generic import (
    ListView,
    CreateView,
)
from core.celery import delete_rejected_comments
from django.urls import reverse_lazy
from .models import Skill, Contact
from blog.models import Post
from portfolio.models import Portfolio

# Create your views here.


class IndexView(ListView):
    model = Skill
    template_name = "index/index.html"
    context_object_name = "skills"
    delete_rejected_comments.delay()

    def get_queryset(self):
        # return all the Skill objects
        return self.model.objects.all()

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        portfolio = Portfolio.objects.all().order_by("-created_date")[:6]
        posts = Post.objects.all().order_by("-created_date")[:6]
        context.update(
            {
                "works": portfolio,
                "posts": posts,
            }
        )
        return context


class ContactView(CreateView):
    model = Contact
    template_name = "index/index.html"
    success_url =  reverse_lazy("website:index")
    # form_class = CreateContactForm
    fields = [
        "name",
        "email",
        "subject",
        "message",
    ]

    def form_valid(self, form):
        return super().form_valid(form)
