import pytest
from httpx import AsyncClient

from main import app, get_current_user
from fastapi.testclient import TestClient


@pytest.mark.anyio
async def test_root_without_token():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 401
    assert response.json() == {
        'detail': 'Not authorized. Please, go to /auth/login'}


def override_get_current_user():
    return {
        'exp': 1679863641,
        'sub': '{"id": "11324815", "email": null, "first_name": null, "last_name": null, "display_name": "3clypse", "picture": "https://avatars.githubusercontent.com/u/11727813?v=4", "provider": "github"}'
    }


def test_root_with_token():
    app.dependency_overrides[get_current_user] = override_get_current_user
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == ['ok']
