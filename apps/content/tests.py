import pytest

from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model

from apps.authentication.fixtures import auto_login_user
from apps.content.fixtures import page_fixture
from apps.content.models import Tag, Page

User = get_user_model()


@pytest.mark.django_db
def test_page_list_view(client, auto_login_user, page_fixture):
    access_token, refresh_token, user = auto_login_user()
    page = page_fixture(user_instance=user)
    url = reverse("content:pages-list")
    response = client.get(url, {}, HTTP_AUTHORIZATION='Token ' + access_token)

    assert response.status_code == 200
    assert response.data["results"][0]["id"] == str(page.id)


@pytest.mark.django_db
def test_page_retrieve_view(client, auto_login_user, page_fixture):
    access_token, refresh_token, user = auto_login_user()
    page = page_fixture(user_instance=user)
    url = reverse("content:pages-detail", kwargs={"pk": str(page.id)})
    response = client.get(url, {}, HTTP_AUTHORIZATION='Token ' + access_token)

    assert response.status_code == 200
    assert response.data["id"] == str(page.id)
    assert response.data["name"] == page.name


@pytest.mark.django_db
def test_page_update_view(client, auto_login_user, page_fixture):
    access_token, refresh_token, user = auto_login_user()
    page = page_fixture(user_instance=user)
    url = reverse("content:pages-detail", kwargs={"pk": str(page.id)})
    response = client.put(
        url,
        data={
            "name": "update page test",
            "description": "test description",
            "owner": str(user.id),
            "tags": [Tag.objects.create(name="games").id]
        },
        content_type="application/json",
        HTTP_AUTHORIZATION='Token ' + access_token
    )

    assert response.status_code == 200
    assert response.data == "update page test"
    assert Page.objects.get(id=page.id).name == "update page test"


@pytest.mark.django_db
def test_page_create_view(client, auto_login_user):
    access_token, refresh_token, user = auto_login_user()
    url = reverse("content:pages-list")
    response = client.post(
        url,
        data={
            "name": "create page test",
            "description": "test description",
            "owner": str(user.id),
            "tags": [Tag.objects.create(name="games").id]
        },
        content_type="application/json",
        HTTP_AUTHORIZATION='Token ' + access_token
    )

    assert response.status_code == 201
    assert response.data["name"] == "create page test"
    assert Page.objects.get(name="create page test").name == "create page test"


@pytest.mark.django_db
def test_page_delete_view(client, auto_login_user, page_fixture):
    access_token, refresh_token, user = auto_login_user()
    page = page_fixture(user_instance=user)
    url = reverse("content:pages-detail", kwargs={"pk": page.id})
    response = client.delete(url, HTTP_AUTHORIZATION='Token ' + access_token)

    try:
        Page.objects.get(id=page.id)
    except ObjectDoesNotExist:
        assert response.status_code == 202


@pytest.mark.django_db
def test_page_make_private_view(client, auto_login_user, page_fixture):
    access_token, refresh_token, user = auto_login_user()
    page = page_fixture(user_instance=user)
    url = reverse("content:pages-make-page-private", kwargs={"uuid": str(page.id)})
    response = client.post(url, HTTP_AUTHORIZATION='Token ' + access_token)

    assert response.status_code == 202
    assert Page.objects.get(id=page.id).is_private == True


@pytest.mark.django_db
def test_page_follow_view(client, auto_login_user, page_fixture):
    access_token, refresh_token, user = auto_login_user()
    page = page_fixture(user_instance=user)
    login_url = reverse("authentication:login")
    user = User.objects.create_user(
        username="loggeduser",
        email="logged_user@gmail.com",
        role="user",
        password="123",
    )
    response_from_login = client.post(
        login_url,
        data={
            "email": user.email,
            "password": "123",
        }
    )
    url = reverse("content:pages-follow", kwargs={"uuid": str(page.id)})
    response = client.get(url, HTTP_AUTHORIZATION='Token ' + response_from_login.data["access"])
    assert user in Page.objects.get(id=page.id).follow_requests.all()

