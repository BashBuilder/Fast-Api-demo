# pyright: reportUnknownVariableType=false, reportUnknownMemberType=false, reportUnusedImport=false
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from app import models
from app.config import settings
from app.database import get_db
from app.main import app
from app.models import Base
from app.oauth2 import create_access_token

SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(autouse=True, scope="function")
def session() -> Generator[Session, None, None]:
  Base.metadata.drop_all(bind=engine)
  Base.metadata.create_all(bind=engine)
  db = TestingSessionLocal()
  try:
    yield db
  finally:
    db.close()


@pytest.fixture(autouse=True, scope="function")
def client(session: Session) -> Generator[TestClient, None, None]:
  def override_get_db() -> Generator[Session, None, None]:
    try:
      yield session
    finally:
      session.close()

  app.dependency_overrides[get_db] = override_get_db
  yield TestClient(app)
  # command.upgrade("head")
  # command.downgrade("base")


@pytest.fixture(scope="function")
def test_user(client: TestClient) -> dict[str, str]:
  user_data = {"email": "test1@test.com", "password": "test"}
  response = client.post("/users/register", json=user_data)
  assert response.status_code == 201
  new_user: dict[str, str] = response.json()
  new_user["password"] = "test"
  return new_user


@pytest.fixture(scope="function")
def token(test_user: dict[str, str]) -> str:
  return create_access_token({"sub": test_user["email"], "user_id": test_user["id"]})


@pytest.fixture(scope="function")
def authorized_client(client: TestClient, token: str) -> TestClient:
  client.headers = {
    **client.headers,  # pyright: ignore[reportUnknownMemberType]
    "Authorization": f"Bearer {token}",
  }

  return client


@pytest.fixture(scope="function")
def test_posts(
  authorized_client: TestClient, test_user: dict[str, str], session: Session
) -> list[models.Post]:
  post_array = [
    {
      "title": "Post 1",
      "content": "This is the first post",
      "user_id": test_user["id"],
    },
    {
      "title": "Post 2",
      "content": "This is the second post",
      "user_id": test_user["id"],
    },
  ]

  def create_post_model(post: dict[str, str]) -> models.Post:
    return models.Post(**post)

  post_map = map(create_post_model, post_array)

  session.add_all(post_map)
  session.commit()
  posts = session.query(models.Post).all()

  return posts
