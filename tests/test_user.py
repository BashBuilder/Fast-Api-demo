# pyright: reportUnknownVariableType=false, reportUnknownMemberType=false, reportUnusedImport=false
from fastapi.testclient import TestClient
from jose import jwt

from app import schema
from app.config import settings

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


def test_login(client: TestClient, test_user: dict[str, str]) -> None:
  response = client.post(
    "/login", data={"username": test_user["email"], "password": test_user["password"]}
  )

  assert response.status_code == 200
  token = schema.Token.model_validate(response.json())
  payload = jwt.decode(
    token.access_token, settings.secret_key, algorithms=[settings.algorithm]
  )
  assert payload["sub"] == test_user["email"]
  assert payload["user_id"] == test_user["id"]
