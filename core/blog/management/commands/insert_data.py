from django.core.management.base import BaseCommand
from faker import Faker
from datetime import datetime
from random import randint
from accounts.models import User, Profile
from ...models import Post, Comment, Category

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
            category = Category.objects.create(
                name = self.fake.last_name()
            )
            for _ in range(10):
                post = Post.objects.create(
                    author = profile,
                    title = self.fake.paragraph(nb_sentences=1),
                    summary= self.fake.paragraph(nb_sentences=3),
                    content = self.fake.paragraph(nb_sentences=10),
                    category = category.set(category),
                    tags = self.fake.last_name(),
                    estimated_time = randint(5,15),
                    counted_views = randint(10,5000),
                    counted_likes = randint(1,500),
                    publish_status = self.fake.boolean(),
                    published_date = datetime.now(),
                )
                for _ in range(5):
                    Comment.objects.create(
                        Post = post,
                        name = self.fake.first_name(),
                        email = self.fake.email(),
                        message = self.fake.paragraph(nb_sentences=1),
                        approved = self.fake.boolean(),
                    )
            