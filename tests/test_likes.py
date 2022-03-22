import pytest
from app import models


# NOTE: this fixtire is userd for testing already liked posts
@pytest.fixture()
def test_like(test_posts, test_user, session):
    new_like = models.Like(user_id=test_user['id'], post_id=test_posts[3].id)
    session.add(new_like)
    session.commit()


def test_like_post(authorized_client, test_posts, test_user):
    res = authorized_client.post(
        "/like/", json={"post_id": test_posts[3].id, "dir": 1})

    assert res.status_code == 201


def test_unauthorized_user_like_post(client, test_posts, test_user):
    res = client.post(
        "/like/", json={"post_id": test_posts[3].id, "dir": 1})

    assert res.status_code == 401


def test_like_post_twice(authorized_client, test_posts, test_user, test_like):
    res = authorized_client.post(
        "/like/", json={"post_id": test_posts[3].id, "dir": 1})

    assert res.status_code == 409


def test_unlike_post(authorized_client, test_posts, test_user, test_like):
    res = authorized_client.post(
        "/like/", json={"post_id": test_posts[3].id, "dir": 0})

    assert res.status_code == 201


def test_unlike_non_existing_post(authorized_client, test_posts):
    res = authorized_client.post(
        "/like/", json={"post_id": test_posts[3].id, "dir": 0})

    assert res.status_code == 409


def test_like_non_existing_post(authorized_client, test_posts, test_user):
    res = authorized_client.post(
        "/like/", json={"post_id": 88888888, "dir": 1})

    assert res.status_code == 404
