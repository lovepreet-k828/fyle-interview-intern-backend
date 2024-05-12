from flask.testing import FlaskClient
import pytest
from core import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_ready_route(client: FlaskClient):
    response = client.get("/")
    assert response.status_code == 200
    assert "status" in response.json
    assert "time" in response.json


def test_error_handling(client: FlaskClient):
    # Test FyleError handling
    response = client.get("/non_existent_route")
    assert response.status_code == 404
    assert "error" in response.json
    assert "message" in response.json
