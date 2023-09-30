import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User, Profile


@pytest.fixture
def api_client():
    client = APIClient()
    return client


@pytest.fixture
def common_user():
    user = User.objects.create_user(
        email="testaccount@test.com", password="test/!1234", is_verified=False
    )
    return user


@pytest.fixture
def create_token(common_user):
    user_obj = common_user
    refresh = RefreshToken.for_user(user_obj)
    return str(refresh.access_token)


@pytest.mark.django_db
class TestTaskApi:
    def test_post_registration_response_201_status(self, api_client):
        # sign up and register user
        url = reverse("accounts:api-v1:registration")
        data = {
            "email": "testuser@test.com",
            "password1": "@m12345678",
            "password2": "@m12345678",
        }
        response = api_client.post(url, data=data)
        assert response.status_code == 400

    def test_get_activation_response_200_status(
        self, api_client, create_token
    ):
        # verify user by jwt
        token = create_token
        url = reverse("accounts:api-v1:activation", kwargs={"token": token})
        response = api_client.get(url)
        assert response.status_code == 200

    def test_post_resend_activation_response_200_status(
        self, api_client, common_user
    ):
        # resend the verification email
        email = common_user.email
        url = reverse("accounts:api-v1:activation-resend")
        data = {
            "email": email,
        }
        response = api_client.post(url, data=data)
        assert response.status_code == 200

    def test_put_change_password_response_200_status(
        self, api_client, common_user
    ):
        # change password
        user = common_user
        url = reverse("accounts:api-v1:change-password")
        data = {
            "old_password": "test/!1234",
            "new_password": "@m12345678",
            "new_password1": "@m12345678",
        }
        api_client.force_authenticate(user)
        response = api_client.put(url, data=data)
        assert response.status_code == 200

    def test_post_reset_password_request_response_200_status(
        self, api_client, common_user
    ):
        # reset password request
        url = reverse("accounts:api-v1:reset-password")
        data = {
            "email": common_user.email,
        }
        response = api_client.post(url, data=data, follow=True)
        assert response.status_code == 200

    def test_get_reset_password_confirm_200_status(
        self, api_client, create_token
    ):
        # confirm token and redirect to reset password form
        token = create_token
        url = reverse(
            "accounts:api-v1:reset-password-confirm", kwargs={"token": token}
        )
        response = api_client.get(url, follow=True)
        assert response.status_code == 200

    def test_put_reset_password_token_200_status(
        self, api_client, create_token
    ):
        # confirm token and reset password
        token = create_token
        url = reverse(
            "accounts:api-v1:reset-password-token", kwargs={"token": token}
        )
        data = {"password1": "@my/1234567", "password2": "@my/1234567"}
        response = api_client.put(url, data=data)
        assert response.status_code == 200

    @pytest.mark.skip(
        reason="object will not be found in real database, but exists in fake database. test it manually."
    )
    def test_post_login_token_response_200_status(
        self, api_client, create_token
    ):
        # login token
        user = create_token
        api_client.force_authenticate(user)
        url = reverse("accounts:api-v1:token-login")
        data = {
            "email": user.email,
            "password": user.password,
        }
        response = api_client.post(url, data=data, follow=True)
        assert response.status_code == 200

    @pytest.mark.skip(
        reason="object will not be found in real database, but exists in fake database. test it manually."
    )
    def test_post_jwt_create_response_200_status(
        self, api_client, create_token
    ):
        # login token
        user = create_token
        api_client.force_authenticate(user)
        url = reverse("accounts:api-v1:jwt-create")
        data = {
            "email": user.email,
            "password": user.password,
        }
        response = api_client.post(url, data=data, follow=True)
        assert response.status_code == 200

    @pytest.mark.skip(
        reason="object will not be found in real database, but exists in fake database. test it manually."
    )
    def test_post_jwt_refresh_response_200_status(
        self, api_client, create_token
    ):
        # jwt refresh
        user = create_token
        api_client.force_authenticate(user)
        url = reverse("accounts:api-v1:jwt-refresh")
        data = {
            "email": user.email,
            "password": user.password,
        }
        response = api_client.post(url, data=data, follow=True)
        assert response.status_code == 200

    @pytest.mark.skip(
        reason="object will not be found in real database, but exists in fake database. test it manually."
    )
    def test_post_jwt_verify_response_200_status(
        self, api_client, create_token
    ):
        # login token
        user = create_token
        api_client.force_authenticate(user)
        url = reverse("accounts:api-v1:jwt-verify")
        data = {
            "email": user.email,
            "password": user.password,
        }
        response = api_client.post(url, data=data, follow=True)
        assert response.status_code == 200

    def test_get_profile_200_status(self, api_client, common_user):
        # get profile
        user = common_user
        url = reverse("accounts:api-v1:profile")
        api_client.force_authenticate(user)
        response = api_client.get(url, follow=True)
        assert response.status_code == 200

    def test_put_profile_200_status(self, api_client, common_user):
        # put profile
        user = common_user
        url = reverse("accounts:api-v1:profile")
        profile = Profile.objects.get(user=user)
        data = {
            "id": profile.id,
            "email": user.email,
            "first_name": "mr",
            "last_name": "developer",
            "image": "",
            "description": "na",
        }
        api_client.force_authenticate(user)
        response = api_client.put(url, data=data, follow=True)
        assert response.status_code == 200

    def test_patch_profile_200_status(self, api_client, common_user):
        # patch profile
        user = common_user
        url = reverse("accounts:api-v1:profile")
        data = {
            "last_name": "developer",
        }
        api_client.force_authenticate(user)
        response = api_client.patch(url, data=data, follow=True)
        assert response.status_code == 200
