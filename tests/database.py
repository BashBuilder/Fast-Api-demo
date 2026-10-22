import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from app.config import settings
from app.database import get_db
from app.main import app
from app.models import Base

SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(autouse=True, scope="function")
def session():
  Base.metadata.drop_all(bind=engine)
  Base.metadata.create_all(bind=engine)
  db = TestingSessionLocal()
  try:
    yield db
  finally:
    db.close()


@pytest.fixture(autouse=True, scope="function")
def client(session: Session):
  def override_get_db():
    try:
      yield session
    finally:
      session.close()

  app.dependency_overrides[get_db] = override_get_db
  yield TestClient(app)
  # command.upgrade("head")
  # command.downgrade("base")
