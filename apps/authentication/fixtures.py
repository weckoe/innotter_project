import pytest

from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def auto_login_user(db, client):
    def make_auto_login(user=None):
        if user is None:
            url = reverse("authentication:login")
            user = User.objects.create_user(
                username="testuser",
                email="test_user@gmail.com",
                role="admin",
                password="123",
            )
            response = client.post(
                url,
                data={
                    "email": user.email,
                    "password": "123",
                }
            )

            return response.data["access"], response.data["refresh"], user

    return make_auto_login
