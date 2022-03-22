from jose import jwt
import pytest
from app import schemas
from app.config import settings


def test_create_user(client):
    res = client.post(
        "/users/", json={"email": "ali@gmail.com", "password": "pass123"})

    new_user = schemas.UserResponse(**res.json())
    assert new_user.email == "ali@gmail.com"
    assert res.status_code == 201


def test_login_user(client, test_user):
    res = client.post(
        "/login", data={"username": test_user['email'], "password": test_user['password']})

    login_res = schemas.TokenResponse(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[
        settings.algorithm])
    id = payload.get("user_id")

    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200


@pytest.mark.parametrize("email, password, status_code",  [
    ("wrongemail@gmail.com", "pass123", 403),
    ("ali@gmail.com", "wrong_password", 403),
    ("wrongemail@gmail.com", "wrong_password", 403),
    (None, "pass123", 422),
    ("ali@gmail.com", None, 422),
])
def test_login_user_wrong_password(client, email, password, status_code):
    res = client.post(
        "/login", data={"username": email, "password": password})

    assert res.status_code == status_code
    # assert res.json().get("detail") == "Invalid username or password"
