import pytest
from core.models.users import User
from core import db
from datetime import datetime
from unittest.mock import patch


@pytest.fixture
def user_data():
    return {"username": "test_user", "email": "test@example.com"}


@pytest.fixture
def add_user(user_data: dict[str, str]):
    user = User(**user_data)
    db.session.add(user)
    db.session.commit()
    yield user
    db.session.delete(user)
    db.session.commit()


def test_user_repr():
    user = User(username="test_user", email="test@example.com")
    assert repr(user) == "<User 'test_user'>"


def test_user_get_by_id(add_user: User):
    user = User.get_by_id(add_user.id)
    assert user.username == "test_user"


def test_user_get_by_email(add_user: User):
    user = User.get_by_email("test@example.com")
    assert user.username == "test_user"
