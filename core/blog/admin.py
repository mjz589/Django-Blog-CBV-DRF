from django.contrib import admin
from .models import Post, Category, Comment


# Register your models here.


# @admin.register(Post)       # alterative way of registering
class PostAdmin(admin.ModelAdmin):
    date_hierarchy = "created_date"
    empty_value_display = "-"
    list_display = (
        "title",
        "author",
        "created_date",
        "publish_status",
        "published_date",
    )
    list_filter = (
        "publish_status",
        "author",
    )
    # ordering = ('-created_date',)
    search_fields = ["title", "content"]


admin.site.register(Post, PostAdmin)
admin.site.register(Category)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    date_hierarchy = "created_date"
    empty_value_display = "-"
    list_display = (
        "email",
        "id",
        "post",
        "approved",
        "created_date",
    )
    list_filter = ("approved",)
    ordering = ("-created_date",)
    search_fields = (
        "post",
        "email",
        "name",
    )
