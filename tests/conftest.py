# NOTE: all the code here is accessable to all the file within the tests package(folder)


import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import models
from app.config import settings
from app.database import get_db, Base
from app.main import app
from app.oauth2 import create_access_token


# NOTE: the test function name must start with test_
# NOTE: parametrize creates multiple value to test
# NOTE: fixture is a decorator(runs before the test runs) that is used to mark a test function as a fixture so that it can be used in other test functions.

# ------------------------------------------------ test db and its fixture ------------------------------------------------
# NOTE: setting up the test database so as to not have to mess with the database(dev or prod)
SQLALCHEMY_DATEBASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATEBASE_URL)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

# ------------------------------------------------ test user fixture ------------------------------------------------


@pytest.fixture
def test_user(client):
    user_data = {"email": "ali@gmail.com",
                 "password": "pass123"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def test_user2(client):
    user_data = {"email": "gael@gmail.com",
                 "password": "pass123"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


# ------------------------------------------------ test posts fixture ------------------------------------------------
@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})


@pytest.fixture
def authorized_client(client, token):
    """adds the token from the token fixture to the header of the request"""
    client.headers = {**client.headers,
                      "Authorization": f"Bearer {token}"
                      }
    return client


@pytest.fixture
def test_posts(test_user, test_user2, session):
    posts_data = [
        {"title": "1st post",
         "content": "1st content",
         "owner_id": test_user["id"]
         },
        {"title": "2nd post",
         "content": "2nd content",
         "owner_id": test_user["id"]
         },
        {"title": "3rd post",
         "content": "3ed content",
         "owner_id": test_user["id"]
         },
        {"title": "4th post",
         "content": "4th content",
         "owner_id": test_user2["id"]
         },
    ]

    def create_post_model(post):
        return models.Post(**post)

    posts_to_models = map(create_post_model, posts_data)
    list_post_models = list(posts_to_models)
    session.add_all(list_post_models)
    session.commit()

    posts = session.query(models.Post).all()
    return posts
# ------------------------------------------------ test comments fixture ------------------------------------------------


@pytest.fixture
def test_comments(test_user, session, test_posts):
    comments_data = [
        {"content": "good 1st post",
         "com_owner_id": test_user["id"],
         "com_post_id": test_posts[0].id
         },
        {"content": "really nice 2nd post",
         "com_owner_id": test_user["id"],
         "com_post_id": test_posts[1].id
         },
        {"content": " very bad 3rd post",
         "com_owner_id": test_user["id"],
         "com_post_id": test_posts[2].id
         },

    ]

    def create_comment_model(comment):
        return models.Comment(**comment)

    comments_to_models = map(create_comment_model, comments_data)
    list_comments_models = list(comments_to_models)
    session.add_all(list_comments_models)
    session.commit()

    comments = session.query(models.Comment).all()
    return comments
