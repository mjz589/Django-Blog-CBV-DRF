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
        category, _ =PortfolioCategory.objects.get_or_create(
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
class TestpostModels:
    def test_get_post_retrieve_response_200_status(
        self, api_client, create_post
    ):
        # show post list after redirecting to login url for authenticatication
        url = reverse("portfolio:detail")
        post = create_post
        response = api_client.get(url)
        assert response.status_code == 200
        assert Portfolio.objects.filter(id=post.id, title=post.title).exists()
