import pytest

from django.urls import reverse

from apps.authentication.fixtures import auto_login_user

from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_user_list_view(client, auto_login_user):
    access_token, refresh_token, user = auto_login_user()

    url = reverse("authentication:users-list")
    response = client.get(url, {}, HTTP_AUTHORIZATION='Token ' + access_token)

    assert response.status_code == 200
    assert response.data["results"][0]["email"] == user.email


@pytest.mark.django_db
def test_user_retrieve_view(client, auto_login_user):
    access_token, refresh_token, user = auto_login_user()

    url = reverse("authentication:users-detail", kwargs={"pk": str(user.id)})
    response = client.get(
        url,
        {},
        HTTP_AUTHORIZATION='Token ' + access_token
    )

    assert response.status_code == 200
    assert response.data["email"] == user.email


@pytest.mark.django_db
def test_user_update_view(client, auto_login_user):
    access_token, refresh_token, user = auto_login_user()

    url = reverse("authentication:users-detail", kwargs={"pk": str(user.id)})
    response = client.put(
        url,
        data={
            "username": "newusername",
            "first_name": "new user",
            "last_name": "new user",
            "email": "new_email@gmail.com",
            "title": "new_user",
        },
        content_type="application/json",
        HTTP_AUTHORIZATION="Token " + access_token
    )
    assert response.status_code == 202
    assert response.data["email"] == User.objects.get(id=user.id).email


@pytest.mark.django_db
def test_user_create_view(client, auto_login_user):
    new_user = {
        "username": "testuser2",
        "email": "test_user2@gmail.com",
        "first_name": "new user",
        "last_name": "new user",
        "role": "user",
        "title": "user title",
        "password": "12345678@",
        "password2": "12345678@"
    }
    access_token, refresh_token, user = auto_login_user()

    url = reverse("authentication:users-list")
    response = client.post(
        url,
        data=new_user,
        content_type="application/json",
        HTTP_AUTHORIZATION="Token " + access_token
    )
    assert response.data["email"] == new_user["email"]
    assert response.data["email"] == User.objects.get(email=new_user["email"]).email


@pytest.mark.django_db
def test_user_block_user_view(client, auto_login_user):
    access_token, refresh_token, user = auto_login_user()

    url = reverse("authentication:users-block-user", kwargs={"id": str(user.id)})
    response = client.post(
        url,
        HTTP_AUTHORIZATION="Token " + access_token
    )

    assert response.status_code == 202
    assert User.objects.get(id=user.id).is_blocked == True
