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
        email="test333@test.com", password="test/!1234",
        is_verified=True, is_active=True,
    )
    profile = Profile.objects.get(user=staff_user)
    profile.first_name = Faker.first_name()
    profile.last_name = Faker.last_name()
    profile.description = Faker.paragraph(nb_sentences=5)
    profile.save()
    return user

@pytest.fixture
def staff_user():
    user = User.objects.create_user(
        email="test333@test.com", password="test/!1234",
        is_verified=True, is_active=True, is_staff=True,
    )
    return user

@pytest.fixture
def create_post(staff_user):
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
    profile.first_name = Faker.first_name()
    profile.last_name = Faker.last_name()
    profile.description = Faker.paragraph(nb_sentences=5)
    profile.save()
    for name in category_list:
        Category.objects.get_or_create(
            name=name,
        )
        post = Post.objects.create(
            author=profile,
            title=Faker.paragraph(nb_sentences=1),
            summary=Faker.paragraph(nb_sentences=3),
            content=Faker.paragraph(nb_sentences=10),
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
                name=Faker.first_name(),
                email=Faker.email(),
                message=Faker.paragraph(nb_sentences=1),
                approved=Faker.boolean(),
            )
    return post

@pytest.fixture
def create_coment(create_post):
    comment = Comment.objects.create(
                    post=create_post,
                    name=Faker.first_name(),
                    email=Faker.email(),
                    message=Faker.paragraph(nb_sentences=1),
                    approved=Faker.boolean(),
                )
    return comment

@pytest.mark.django_db
class TestpostApi:
    def test_get_post_list_response_200_status(self, api_client):
        # show post list
        url = reverse("blog:api-v1:post-list")
        response = api_client.get(url)
        assert response.status_code == 200

    def test_post_post_create_response_201_status(
        self, api_client, common_user
    ):
        # craete a post after redirecting to login url for authenticatication
        user = common_user
        url = reverse("blog:api-v1:post-list")
        api_client.force_authenticate(user)
        data = {
            "author": user,
            "title": "test",
            "summary": "summary description is here.",
            "content": "They are not passed to workflows that are triggered by a pull request from a fork.",
            "category": [1,3,4],
            "tags": ["post",],
            "estimated_time": 12,
            "published_date": "2023-10-13T21:00:00.859567+03:30"
        }
        response = api_client.post(url, data=data, follow=True)
        assert response.status_code == 201

    def test_get_post_retrieve_response_200_status(
        self, api_client, common_user, create_post
    ):
        # retrieve a single post after redirecting to login url for authenticatication
        user = common_user
        url = reverse("blog:api-v1:post-detail", kwargs={"pk": create_post.id})
        api_client.force_authenticate(user)
        response = api_client.get(url, follow=True)
        assert response.status_code == 200

    def test_put_post_response_200_status(
        self, api_client, common_user, create_post
    ):
        # edit(put) a post after redirecting to login url for authenticatication
        user = common_user
        url = reverse("blog:api-v1:post-detail", kwargs={"pk": create_post.id})
        api_client.force_authenticate(user)
        data = {
            "user": user,
            "title": "Testpost-edited",
            "complete": False,
        }
        response = api_client.put(url, data=data, follow=True)
        assert response.status_code == 200

    def test_patch_post_response_200_status(
        self, api_client, common_user, create_post
    ):
        # edit(patch) a post after redirecting to login url for authenticatication
        user = common_user
        url = reverse("blog:api-v1:post-detail", kwargs={"pk": create_post.id})
        api_client.force_authenticate(user)
        data = {
            "complete": False,
        }
        response = api_client.patch(url, data=data, follow=True)
        assert response.status_code == 200

    def test_delete_post_response_204_status(
        self, api_client, common_user, create_post
    ):
        # delete a post after redirecting to login url for authenticatication
        user = common_user
        url = reverse("blog:api-v1:post-detail", kwargs={"pk": create_post.id})
        api_client.force_authenticate(user)
        response = api_client.delete(url, follow=True)
        assert response.status_code == 204
