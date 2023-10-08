from django.shortcuts import render,get_object_or_404 , HttpResponseRedirect, redirect

from django.utils import timezone
from .models import *
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from blog.forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from accounts.models import User, Profile
from django.views.generic import (
    View,
    ListView,
    DetailView,
    CreateView,
)
# Create your views here.

def blog_view(request, **kwargs):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

    for post in posts: # turn publish_status on(Ture) if published_date is passed
        if post.publish_status == False:
            post.publish_status = True
            post.save() 

    if kwargs.get('cat_name') != None:  # posts by category
        posts = posts.filter(category__name=kwargs['cat_name'])

    if kwargs.get('author_username') != None:
        posts = posts.filter(author__username=kwargs['author_username'])
    
    if kwargs.get('tag_name') != None:
        posts = posts.filter(tags__name__in=[kwargs['tag_name']])


    # pagination
    posts = Paginator(posts, 3)
    try :
        page_number = request.GET.get('page')
        posts = posts.get_page(page_number)
    except PageNotAnInteger:
        posts = posts.get_page(1)
    except EmptyPage:
        posts = posts.get_page(1)



    context={'posts': posts}
    return render(request, 'blog/blog-home.html', context)


class BlogList(ListView):
    model = Post
    template_name = "blog/blog-list.html"
    context_object_name = "posts"

    def get_queryset(self, **kwargs):
        # return all the comment objects from a specified post
        posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

        for post in posts: # turn publish_status on(Ture) if published_date is passed
            if post.publish_status == False:
                post.publish_status = True
                post.save()
        if kwargs.get('cat_name') != None:  # posts by category
            posts = posts.filter(category__name=kwargs['cat_name'])

        if kwargs.get('author_username') != None:
            posts = posts.filter(author__username=kwargs['author_username'])
        
        if kwargs.get('tag_name') != None:
            posts = posts.filter(tags__name__in=[kwargs['tag_name']])
        return posts


class BlogDetail(ListView):
    model = Comment
    template_name = "blog/blog-details.html"
    context_object_name = "comments"

    def get_queryset(self):
        # return all the comment objects from a specified post
        post_id = self.kwargs['pk']
        post = Post.objects.get(id=post_id)
        return self.model.objects.filter(post=post,approved=True)
    
    def get_context_data(self, **kwargs):
        context = super(BlogDetail, self).get_context_data(**kwargs)
        post = Post.objects.get(id=self.kwargs['pk'])
        context.update(
            {
                "post": post,
            }
        )
        return context
    
class CommentCreate(CreateView):
    model = Comment
    template_name = "blog/blog-details.html"
    fields = ['message', 'name', 'email',]

    def form_valid(self, form):
        form.instance.post = Post.objects.get(id=self.kwargs['pk'])
        return super().form_valid(form)
    
class BlogSearch(ListView):
    model = Post
    template_name = "blog/blog-home.html"
    context_object_name = "comments"

    def get_queryset(self):
        # return all related posts
        posts =Post.objects.filter(published_date__lte=timezone.now())
        if s := self.request.GET.get('s'):
            posts = posts.filter(summary__contains=s) | posts.filter(title__contains=s)
        return posts
