# pyright: reportUnknownVariableType=false, reportUnknownMemberType=false, reportUnusedImport=false

from fastapi.testclient import TestClient


def test_get_all_posts(authorized_client: TestClient) -> None:
  response = authorized_client.get("/posts")

  assert response.status_code == 200
