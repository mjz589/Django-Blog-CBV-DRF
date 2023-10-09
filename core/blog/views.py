from django.shortcuts import render,get_object_or_404 , HttpResponseRedirect, redirect

from django.utils import timezone
from .models import *
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from blog.forms import CommentForm
from django.contrib import messages
from django.views.generic import (
    ListView,
    CreateView,
)
# Create your views here.


class BlogList(ListView):
    model = Post
    template_name = "blog/blog-list.html"
    context_object_name = "posts"

    def get_queryset(self):
        # return all the comment objects from a specified post
        posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

        for post in posts: # turn publish_status on(Ture) if published_date is passed
            if post.publish_status == False:
                post.publish_status = True
                post.save()
        if self.kwargs.get('cat_name') != None:  # posts by category
            posts = posts.filter(category__name=self.kwargs['cat_name'])

        # if kwargs.get('author_username') != None:
        #     posts = posts.filter(author__username=kwargs['author_username'])
        
        if self.kwargs.get('tag_name') != None:
            posts = posts.filter(tags__name__in=[self.kwargs['tag_name']])
        return posts
    
    paginate_by = 7

    def get_context_data(self, **kwargs):
        context = super(BlogList, self).get_context_data(**kwargs)
        if not context.get("is_paginated", False):
            return context
        # Custom Pagination
        paginator = context.get("paginator")
        num_pages = paginator.num_pages
        current_page = context.get("page_obj")
        page_no = current_page.number

        if num_pages <= 5 or page_no <= 3:  # case 1 and 2
            pages = [x for x in range(1, min(num_pages + 1, 5))]
        elif page_no > num_pages - 3:  # case 4
            pages = [x for x in range(num_pages - 4, num_pages + 1)]
        else:  # case 3
            pages = [x for x in range(page_no - 2, page_no + 3)]

        # previous page and first page
        if page_no == 1:
            previous_page = 1
            first_page = 1
        else:
            previous_page = pages[page_no - 1] - 1
            first_page = pages[0]

        # next page and last page
        if page_no == pages[-1]:
            next_page = page_no
            last_page = 1
        else:  # page_no ==1  , pages[page_no] == 2 , pages[page_no] +1 = 3
            next_page = pages[page_no - 1] + 1
            last_page = pages[-1]
        page_count = len(pages)
        context.update(
            {
                "pages": pages,
                "first_page": first_page,
                "last_page": last_page,
                "previous_page": previous_page,
                "next_page": next_page,
                "current_page": page_no,
                "page_count": page_count,
            }
        )
        return context

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
    template_name = "blog/blog-list.html"
    context_object_name = "posts"

    def get_queryset(self):
        # return all related posts
        posts =Post.objects.filter(published_date__lte=timezone.now())
        if s := self.request.GET.get('s'):
            posts = posts.filter(summary__contains=s) | posts.filter(title__contains=s)
        return posts
