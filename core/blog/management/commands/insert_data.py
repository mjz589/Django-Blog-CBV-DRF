from django.core.management.base import BaseCommand
from faker import Faker
from django.utils import timezone
from random import randint, choices
from accounts.models import User, Profile
from ...models import Post, Comment, Category

category_list = [
    "IT",
    "design",
    "development",
    "backend",
    "frontend",
]
tag_list = [
    "django",
    "python",
    "sql",
    "nginx",
    "restframework",
    "C++",
    "C#",
]


# fake posts and comments data
class Command(BaseCommand):
    help = "inserting dummy data into database: post and comment"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fake = Faker()

    def handle(self, *args, **kwargs):
        # creating dummy data
        for _ in range(10):
            user = User.objects.create_user(
                email=self.fake.email(),
                password="fake@1234",
                is_active=True,
                is_verified=True,
            )
            profile = Profile.objects.get(user=user)
            profile.first_name = self.fake.first_name()
            profile.last_name = self.fake.last_name()
            profile.description = self.fake.paragraph(nb_sentences=5)
            profile.save()
            for name in category_list:
                Category.objects.get_or_create(
                    name=name,
                )
            for _ in range(10):
                post = Post.objects.create(
                    author=profile,
                    title=self.fake.paragraph(nb_sentences=1),
                    summary=self.fake.paragraph(nb_sentences=3),
                    content=self.fake.paragraph(nb_sentences=10),
                    estimated_time=randint(5, 15),
                    counted_views=randint(10, 5000),
                    counted_likes=randint(1, 500),
                    publish_status=True,
                    published_date=timezone.now(),
                )
                # many to many fields : category - tags
                category_name = choices(category_list, k=3)[
                    0
                ]  # Extract the category name from the tuple
                category, _ = Category.objects.get_or_create(name=category_name)
                tags = (choices(tag_list, k=2),)
                post.category.set([category])
                post.tags.set(*tags)
                for _ in range(5):
                    Comment.objects.create(
                        post=post,
                        name=self.fake.first_name(),
                        email=self.fake.email(),
                        message=self.fake.paragraph(nb_sentences=1),
                        approved=self.fake.boolean(),
                    )
