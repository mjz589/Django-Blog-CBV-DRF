from django.core.management.base import BaseCommand
from faker import Faker

from accounts.models import User, Profile
from ...models import Task


class Command(BaseCommand):
    help = "inserting dummy data into database"

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
            for _ in range(10):
                Task.objects.create(
                    user=profile,
                    title=self.fake.paragraph(nb_sentences=1),
                    complete=self.fake.boolean(),
                )
