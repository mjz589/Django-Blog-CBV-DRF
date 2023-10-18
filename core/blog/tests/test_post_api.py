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
        email="admin@admin.com",
        password="test/!1234",
        is_active=True,
        is_verified=True,
    )
    return user


@pytest.fixture
def staff_user():
    user = User.objects.create_user(
        email="blog.api.admin@test.com",
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

    def test_get_post_list_response_200_status(self, api_client):
        # show post list
        url = reverse("blog:api-v1:post-list")
        response = api_client.get(url)
        assert response.status_code == 200

    def test_post_post_create_response_201_status(self, api_client, staff_user):
        # craete a post after redirecting to login url for authenticatication
        user = staff_user
        url = reverse("blog:api-v1:post-list")
        categories = TestpostApi.category_list
        categories_id = []
        for cat in categories:
            category, _ = Category.objects.get_or_create(name=cat)
            categories_id.append(category.id)
        api_client.force_authenticate(user)
        data = {
            "author": user,
            "title": "string",
            "summary": "string",
            "content": "string",
            "category": categories_id,
            "tags": [
                "sql",
                "nginx",
                "restframework",
            ],
            "estimated_time": 5,
            "published_date": "2023-10-16T16:42:18.631Z",
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

    def test_put_post_response_200_status(self, api_client, staff_user, create_post):
        # edit(put) a post after redirecting to login url for authenticatication
        user = staff_user
        categories = TestpostApi.category_list
        categories_id = []
        for cat in categories:
            category, _ = Category.objects.get_or_create(name=cat)
            categories_id.append(category.id)
        url = reverse("blog:api-v1:post-detail", kwargs={"pk": create_post.id})
        api_client.force_authenticate(user)
        data = {
            "author": user,
            "title": "title edited",
            "summary": "summary edited",
            "content": "content edited",
            "category": categories_id,
            "estimated_time": 2,
            "published_date": "2023-10-16T16:42:18.631Z",
        }
        response = api_client.put(url, data=data, follow=True)
        assert response.status_code == 200

    def test_patch_post_response_200_status(self, api_client, staff_user, create_post):
        # edit(patch) a post after redirecting to login url for authenticatication
        user = staff_user
        categories = TestpostApi.category_list
        categories_id = []
        for cat in categories:
            category, _ = Category.objects.get_or_create(name=cat)
            categories_id.append(category.id)
        url = reverse("blog:api-v1:post-detail", kwargs={"pk": create_post.id})
        api_client.force_authenticate(user)
        data = {
            "complete": False,
        }
        response = api_client.patch(url, data=data, follow=True)
        assert response.status_code == 200

    def test_delete_post_response_204_status(self, api_client, staff_user, create_post):
        # delete a post after redirecting to login url for authenticatication
        user = staff_user
        url = reverse("blog:api-v1:post-detail", kwargs={"pk": create_post.id})
        api_client.force_authenticate(user)
        response = api_client.delete(url, follow=True)
        assert response.status_code == 204
