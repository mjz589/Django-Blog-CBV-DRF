from rest_framework import serializers
from ...models import Task
from accounts.models import Profile


class TaskSerializer(serializers.ModelSerializer):
    # show user profile image url
    image = serializers.SerializerMethodField(
        method_name="get_image", read_only=True
    )

    relative_url = serializers.URLField(
        source="get_absolute_api_url", read_only=True
    )
    absolute_url = serializers.SerializerMethodField(method_name="get_abs_url")

    def get_abs_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.pk)

    # how to represent objects
    def to_representation(self, instance):
        request = self.context.get("request")
        rep = super().to_representation(instance)
        # show user as first name
        rep["user"] = instance.user.user.email

        # seperate list and detail for display
        if request.parser_context.get("kwargs").get("pk"):
            rep.pop("relative_url", None)
            rep.pop("absolute_url", None)
        else:
            rep.pop("created_date", None)
        # if instance has a category
        """rep['category'] = CategorySerializer(instance.category,context={'request':request}).data """
        return rep

    # get user image from profile
    def get_image(self, instance):
        request = self.context.get("request")
        image_url = instance.user.image.url
        return request.build_absolute_uri(image_url)

    # user must automatically be provided and not be written by users
    """ you can do it like this:
        user = serializers.PrimaryKeyRelatedField(read_only=True)
        or do it another way:  """

    def create(self, validated_data):
        validated_data["user"] = Profile.objects.get(
            user__id=self.context.get("request").user.id
        )
        return super().create(validated_data)

    class Meta:
        model = Task
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
        read_only_fields = (
            "author",
            "image",
            "counted_views",
            "counted_likes"
        )
