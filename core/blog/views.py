from django.utils import timezone

# from django.contrib import messages
from django.views.generic import (
    ListView,
    CreateView,
)
from .models import Post, Comment

# from blog.forms import CommentForm

# Create your views here.


class BlogList(ListView):
    model = Post
    template_name = "blog/blog-list.html"
    context_object_name = "posts"

    def get_queryset(self):
        # return all the comment objects from a specified post
        posts = Post.objects.filter(published_date__lte=timezone.now()).order_by(
            "-published_date"
        )

        for post in posts:  # turn publish_status on(Ture) if published_date is passed
            if post.publish_status is False:
                post.publish_status = True
                post.save()
        if self.kwargs.get("cat_name") is not None:  # posts by category
            posts = posts.filter(category__name=self.kwargs["cat_name"])

        # if kwargs.get('author_username') != None:
        #     posts = posts.filter(author__username=kwargs['author_username'])

        if self.kwargs.get("tag_name") is not None:
            posts = posts.filter(tags__name__in=[self.kwargs["tag_name"]])
        return posts

    paginate_by = 6

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

        # first and last page
        first_page = 1
        last_page = num_pages

        context.update(
            {
                "pages": pages,
                "first_page": first_page,
                "last_page": last_page,
                "current_page": page_no,
                "page_count": num_pages,
            }
        )
        return context


class BlogDetail(ListView):
    model = Comment
    template_name = "blog/blog-details.html"
    context_object_name = "comments"

    def get_queryset(self, request):
        # return all the comment objects from a specified post
        post_id = self.kwargs["pk"]
        post = Post.objects.get(id=post_id)
        return self.model.objects.filter(post=post, approved=True)

    def get_context_data(self, **kwargs):
        context = super(BlogDetail, self).get_context_data(**kwargs)
        post = Post.objects.get(id=self.kwargs["pk"])
        context.update(
            {
                "post": post,
            }
        )
        return context


class CommentCreate(CreateView):
    model = Comment
    template_name = "blog/blog-details.html"
    fields = [
        "message",
        "name",
        "email",
    ]

    def form_valid(self, form):
        form.instance.post = Post.objects.get(id=self.kwargs["pk"])
        return super().form_valid(form)


class BlogSearch(ListView):
    model = Post
    template_name = "blog/blog-list.html"
    context_object_name = "posts"

    def get_queryset(self):
        # return all related posts
        posts = Post.objects.filter(published_date__lte=timezone.now())
        if s := self.request.GET.get("s"):
            posts = posts.filter(summary__contains=s) | posts.filter(title__contains=s)
        return posts
