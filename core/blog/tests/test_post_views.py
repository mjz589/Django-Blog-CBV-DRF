import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from django.utils import timezone
from faker import Faker
from random import randint, choices
from accounts.models import User, Profile
from blog.models import Post, Category, Comment


@pytest.fixture
def api_client():
    client = APIClient()
    return client


@pytest.fixture
def common_user():
    user = User.objects.create_user(
        email="blog.test.views@test.com",
        password="test/!1234",
        is_verified=True,
        is_active=True,
    )
    return user


@pytest.fixture
def staff_user():
    user = User.objects.create_user(
        email="blog.views.admin@test.com",
        password="test/!1234",
        is_verified=True,
        is_active=True,
        is_staff=True,
    )
    return user


@pytest.fixture
def create_post(staff_user):
    fake = Faker()
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
    profile = Profile.objects.get(user=staff_user)
    profile.first_name = fake.first_name()
    profile.last_name = fake.last_name()
    profile.description = fake.paragraph(nb_sentences=1)
    profile.save()
    for name in category_list:
        Category.objects.get_or_create(
            name=name,
        )
        post = Post.objects.create(
            author=profile,
            title=fake.paragraph(nb_sentences=1),
            summary=fake.paragraph(nb_sentences=3),
            content=fake.paragraph(nb_sentences=10),
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
                name=fake.first_name(),
                email=fake.email(),
                message=fake.paragraph(nb_sentences=1),
                approved=fake.boolean(),
            )
    return post


@pytest.mark.django_db
class TestpostModels:
    def test_get_post_list_response_200_status(
        self, api_client, common_user, create_post
    ):
        # show post list after redirecting to login url for authenticatication
        url = reverse("blog:index")
        post = create_post
        response = api_client.get(url)
        assert response.status_code == 200
        assert Post.objects.filter(id=post.id, title=post.title).exists()

    # def test_post_post_create_response_200_status(
    #     self, api_client, common_user
    # ):
    #     # craete a post after redirecting to login url for authenticatication
    #     user = common_user
    #     url = reverse("blog:post_list")
    #     api_client.force_authenticate(user)
    #     data = {
    #         "user": user,
    #         "title": "Testpost-created",
    #         "complete": True,
    #     }
    #     response = api_client.post(url, data=data, follow=True)
    #     assert response.status_code == 200

    # def test_patch_post_complete_response_200_status(
    #     self, api_client, common_user, create_post
    # ):
    #     # make a post complete true value after redirecting to login url for authenticatication
    #     user = common_user
    #     url = reverse("blog:complete_post", kwargs={"pk": create_post.id})
    #     api_client.force_authenticate(user)
    #     data = {
    #         "complete": True,
    #     }
    #     response = api_client.patch(url, data=data, follow=True)
    #     assert response.status_code == 200

    # def test_patch_post_rename_response_200_status(
    #     self, api_client, common_user, create_post
    # ):
    #     # make a post complete true value after redirecting to login url for authenticatication
    #     user = common_user
    #     url = reverse("blog:complete_post", kwargs={"pk": create_post.id})
    #     api_client.force_authenticate(user)
    #     data = {
    #         "title": "post renamed",
    #     }
    #     response = api_client.patch(url, data=data, follow=True)
    #     assert response.status_code == 200

    # def test_delete_post_response_200_status(
    #     self, api_client, common_user, create_post
    # ):
    #     # delete a post after redirecting to login url for authenticatication
    #     user = common_user
    #     url = reverse("blog:delete_post", kwargs={"pk": create_post.id})
    #     api_client.force_authenticate(user)
    #     response = api_client.delete(url, follow=True)
    #     assert response.status_code == 200
