import pytest

from apps.content.models import Page
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def page_fixture(db, client):
    def create_page(user_instance=None):
        page = Page.objects.create(
            name="test page",
            description="test description",
            owner=user_instance,
        )

        page.followers.add(
            User.objects.create_user(
                username="follower_for_test_page",
                email="follower_for_test_page@gmail.com",
                role="user",
                password="123",
            )
        )
        page.follow_requests.add(
            User.objects.create_user(
                username="follow_request_user_for_test_page",
                email="follow_request_user_for_test_page@gmail.com",
                role="user",
                password="123",
            )
        )
        page.save()
        return page

    return create_page
