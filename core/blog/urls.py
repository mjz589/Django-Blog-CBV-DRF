from django.urls import path, include
from blog.views import (
    BlogList,
    BlogDetail,
    CommentCreate,
    BlogSearch,
)
from blog.feeds import LatestEntriesFeed

app_name  = 'blog'

urlpatterns = [

    path('' , BlogList.as_view(), name='index'),
    path('<int:pk>', BlogDetail.as_view(), name='detail'),
    path('<int:pk>/comment-create', CommentCreate.as_view(), name='comment-create'),
    path('category/<str:cat_name>' , BlogList.as_view(), name='category'),
    path('tag/<str:tag_name>' , BlogList.as_view(), name='tag'),
    # path('author/<str:author_username>' , BlogList.as_view(), name='author'),
    path('search/', BlogSearch.as_view(), name='search'),
    path('rss/feed/', LatestEntriesFeed()),

    path("api/v1/", include("blog.api.v1.urls")),
]
