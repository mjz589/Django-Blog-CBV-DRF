from django_filters import rest_framework as filters
from taggit.managers import TaggableManager
from blog.models import Post


class PostFilter(filters.FilterSet):
    tags = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Post
        fields = ["category", "tags"]
        
        filter_overrides = {
            TaggableManager: {
                'filter_class': filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
        }