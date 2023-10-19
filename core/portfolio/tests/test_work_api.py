import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from django.utils import timezone
from faker import Faker
from random import choice
from accounts.models import User, Profile
from portfolio.models import Portfolio, PortfolioCategory


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
        email="portfolio.api.admin@test.com",
        password="test/!1234",
        is_verified=True,
        is_active=True,
        is_staff=True,
    )
    return user


@pytest.fixture
def create_work(staff_user):
    fake = Faker()
    category_list = [
        "IT",
        "design",
        "development",
        "backend",
        "frontend",
    ]
    profile = Profile.objects.get(user=staff_user)
    profile.first_name = fake.first_name()
    profile.last_name = fake.last_name()
    profile.description = fake.paragraph(nb_sentences=1)
    profile.save()
    cat_list = []
    for name in category_list:
        category, _ = PortfolioCategory.objects.get_or_create(
            name=name,
        )
        cat_list.append(category)

    work = Portfolio.objects.create(
        title=fake.paragraph(nb_sentences=1),
        description=fake.paragraph(nb_sentences=5),
        category=choice(cat_list),
        client="CEO",
        project_date=timezone.now(),
        project_url="https://www.mmd-javad.ir"
    )
    return work


@pytest.mark.django_db
class TestworkApi:
    category_list = [
        "IT",
        "design",
        "development",
        "backend",
        "frontend",
    ]

    def test_get_work_list_response_200_status(self, api_client):
        # show work list
        url = reverse("portfolio:api-v1:work-list")
        response = api_client.get(url)
        assert response.status_code == 200

    def test_work_work_create_response_201_status(self, api_client, staff_user):
        # craete a work after redirecting to login url for authenticatication
        user = staff_user
        url = reverse("portfolio:api-v1:work-list")
        categories = TestworkApi.category_list
        category, _ = PortfolioCategory.objects.get_or_create(name=categories[1])
        api_client.force_authenticate(user)
        data = {
            "title": "test-work",
            "description": "test-description",
            "category": category.id,
            "client": "someone",
            "project_date": "2023-10-13T23:29:56+03:30",
            "project_url": "https://themikey.ir"
        }
        response = api_client.post(url, data=data, follow=True)
        assert response.status_code == 201

    def test_get_work_retrieve_response_200_status(
        self, api_client, create_work
    ):
        # retrieve a single work
        url = reverse("portfolio:api-v1:work-detail", kwargs={"pk": create_work.id})
        response = api_client.get(url, follow=True)
        assert response.status_code == 200

    def test_put_work_response_200_status(self, api_client, staff_user, create_work):
        # edit(put) a work after redirecting to login url for authenticatication
        user = staff_user
        categories = TestworkApi.category_list
        categories = TestworkApi.category_list
        category, mmd = PortfolioCategory.objects.get_or_create(name=categories[1])
        url = reverse("portfolio:api-v1:work-detail", kwargs={"pk": create_work.id})
        api_client.force_authenticate(user)
        data = {
            "title": "test-work-edited",
            "description": "test-description edited",
            "category": category.id,
            "client": "someone edited",
            "project_date": "2023-10-13T23:29:56+03:30",
            "project_url": "https://themikey.ir"
        }
        response = api_client.put(url, data=data, follow=True)
        assert response.status_code == 200

    def test_patch_work_response_200_status(self, api_client, staff_user, create_work):
        # edit(patch) a work after redirecting to login url for authenticatication
        user = staff_user
        categories = TestworkApi.category_list
        categories_id = []
        for cat in categories:
            category, _ = PortfolioCategory.objects.get_or_create(name=cat)
            categories_id.append(category)
        url = reverse("portfolio:api-v1:work-detail", kwargs={"pk": create_work.id})
        api_client.force_authenticate(user)
        data = {
            "category": choice(categories_id).id,
            "client": "someone edited",
        }
        response = api_client.patch(url, data=data, follow=True)
        assert response.status_code == 200

    def test_delete_work_response_204_status(self, api_client, staff_user, create_work):
        # delete a work after redirecting to login url for authenticatication
        user = staff_user
        url = reverse("portfolio:api-v1:work-detail", kwargs={"pk": create_work.id})
        api_client.force_authenticate(user)
        response = api_client.delete(url, follow=True)
        assert response.status_code == 204
