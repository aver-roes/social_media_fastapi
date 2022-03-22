import pytest
from app import schemas


def test_get_all_comments(authorized_client, test_posts, test_comments):
    res = authorized_client.get("/comments/")

    assert len(res.json()) == len(test_comments)
    assert res.status_code == 200


def test_unauthorized_user_get_all_comments(client, test_comments):
    res = client.get("/comments/")

    assert res.status_code == 401


@pytest.mark.parametrize("content, com_owner_id, com_post_id", [
    ("good post", 1, 1),
    ("ver nice ", 1, 2),
    ("bad post", 1, 3),
])
def test_create_comments(authorized_client, test_user, test_posts, test_comments, content, com_owner_id, com_post_id):
    res = authorized_client.post(
        "/comments/", json={"content": content, "com_owner_id": com_owner_id, "com_post_id": com_post_id})

    created_comment = schemas.CommentResponse(**res.json())
    assert created_comment.content == content
    assert created_comment.com_owner_id == test_user['id']
    assert res.status_code == 201


def test_unauthorized_user_create_comments(client, test_comments):
    res = client.get("/comments/", json={"content": "random content",
                     "com_owner_id": 1, "com_post_id": 1})

    assert res.status_code == 401


def test_unauthorized_user_delete_comments(client, test_comments):
    res = client.delete(
        f"/posts/{test_comments[0].id}")

    assert res.status_code == 401


def test_delete_comment(authorized_client, test_comments, test_user):
    res = authorized_client.delete(
        f"/comments/{test_comments[0].id}")

    assert res.status_code == 204


def test_delete_comment_non_exist(authorized_client, test_comments, test_user):
    res = authorized_client.delete(
        f"/comments/897979")

    assert res.status_code == 404
