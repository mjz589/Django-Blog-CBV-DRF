from django.urls import path
from blog.views import *
from blog.feeds import LatestEntriesFeed

app_name  = 'blog'

urlpatterns = [

    path('' , blog_view, name='index'),
    path('<int:pk>', BlogDetail.as_view(), name='detail'),
    path('<int:pk>/comment-create', CommentCreate.as_view(), name='comment-create'),
    path('category/<str:cat_name>' , blog_view, name='category'),
    path('tag/<str:tag_name>' , blog_view, name='tag'),
    path('author/<str:author_username>' , blog_view, name='author'),
    path('search/', blog_search, name='search'),
    path('rss/feed/', LatestEntriesFeed()),
]
