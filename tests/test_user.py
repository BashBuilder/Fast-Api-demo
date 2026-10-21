# pyright: reportUnknownVariableType=false, reportUnknownMemberType=false, reportUnusedImport=false
from fastapi.testclient import TestClient

from app import schema

from .database import client, session  # noqa: F401


def test_root(client: TestClient) -> None:
  response = client.get("/")
  assert response.status_code == 200
  assert response.json() == {"message": "Hello World"}


def test_register(client: TestClient) -> None:
  response = client.post(
    "/users/register", json={"email": "test1@test.com", "password": "test"}
  )

  assert response.status_code == 201
  new_user = schema.UserResponse.model_validate(response.json())
  assert new_user.email == "test1@test.com"
  assert new_user.id is not None


def test_login(client: TestClient) -> None:
  response = client.post(
    "/login", json={"username": "test1@test.com", "password": "test"}
  )

  assert response.status_code == 200
  token = schema.Token.model_validate(response.json())
  assert token.access_token is not None
  assert token.token_type is not None
