from rest_framework import serializers

from ...models import Post, Comment, Category
from accounts.models import Profile


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "name",
        ]


class PostSerializer(serializers.ModelSerializer):
    # show image url
    image = serializers.SerializerMethodField(method_name="get_image", read_only=True)
    # show post comments
    comments = serializers.SerializerMethodField(
        method_name="get_comments",
    )
    # show post tags
    # tags = serializers.PrimaryKeyRelatedField(
    #     queryset=Post.objects.all().values_list('tags'), many=True
    # )
    tags = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")

    relative_url = serializers.URLField(source="get_absolute_api_url", read_only=True)
    absolute_url = serializers.SerializerMethodField(method_name="get_abs_url")

    def get_abs_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.pk)

    # how to represent objects
    def to_representation(self, instance):
        request = self.context.get("request")
        rep = super().to_representation(instance)
        # show user as first name
        rep["author"] = instance.author.user.email
        # show category
        rep["category"] = CategorySerializer(
            instance.category, context={"request": request}, many=True
        ).data
        # seperate list and detail for display
        if request.parser_context.get("kwargs").get("pk"):
            rep.pop("relative_url", None)
            rep.pop("absolute_url", None)
        else:
            rep.pop("created_date", None)
        return rep

    # get user image from profile
    def get_image(self, instance):
        request = self.context.get("request")
        image_url = instance.image.url
        return request.build_absolute_uri(image_url)

    def get_comments(self, instance):
        comments = Comment.objects.filter(post=instance, approved=True).values(
            "id",
            "post_id",
            "name",
            "email",
            "message",
            "created_date",
        )
        return comments

    # user must automatically be provided and not be written by users
    """ you can do it like this:
        user = serializers.PrimaryKeyRelatedField(read_only=True)
        or do it another way:  """

    def create(self, validated_data):
        if self.context.get("request") and self.context.get("request").user.is_staff:
            validated_data["author"] = Profile.objects.get(
                user__id=self.context.get("request").user.id
            )
            return super().create(validated_data)
        else:
            raise serializers.ValidationError({"detail": "You must be a staff user"})

    class Meta:
        model = Post
        fields = (
            "id",
            "author",
            "image",
            "title",
            "summary",
            "content",
            "audio",
            "video",
            "category",
            "tags",
            "estimated_time",
            "counted_views",
            "counted_likes",
            "comments",
            "relative_url",
            "absolute_url",
            "published_date",
        )
        read_only_fields = ("author", "image", "counted_views", "counted_likes")
