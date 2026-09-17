import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


def create_card(client, title="Buy milk", description="2% please"):
    return client.post("/api/cards", json={"title": title, "description": description})


# --- GET /api/cards ---------------------------------------------------


def test_list_cards_empty(client):
    response = client.get("/api/cards")
    assert response.status_code == 200
    assert response.json() == []


def test_list_cards_sorted_by_created_at(client):
    create_card(client, title="First")
    create_card(client, title="Second")
    create_card(client, title="Third")

    response = client.get("/api/cards")
    assert response.status_code == 200
    titles = [card["title"] for card in response.json()]
    assert titles == ["First", "Second", "Third"]


# --- POST /api/cards ----------------------------------------------------


def test_create_card_returns_full_card(client):
    response = create_card(client, title="Write tests", description="Cover every endpoint")
    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "Write tests"
    assert body["description"] == "Cover every endpoint"
    assert body["status"] == "todo"
    assert isinstance(body["id"], int)
    assert "created_at" in body


def test_create_card_defaults_description_to_empty_string(client):
    response = client.post("/api/cards", json={"title": "No description"})
    assert response.status_code == 201
    assert response.json()["description"] == ""


def test_create_card_trims_whitespace(client):
    response = client.post(
        "/api/cards", json={"title": "  Padded title  ", "description": "  padded desc  "}
    )
    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "Padded title"
    assert body["description"] == "padded desc"


def test_create_card_missing_title_is_422(client):
    response = client.post("/api/cards", json={"description": "no title given"})
    assert response.status_code == 422


def test_create_card_empty_title_is_422(client):
    response = client.post("/api/cards", json={"title": ""})
    assert response.status_code == 422


def test_create_card_whitespace_only_title_is_422(client):
    response = client.post("/api/cards", json={"title": "   "})
    assert response.status_code == 422


def test_create_card_title_too_long_is_422(client):
    response = client.post("/api/cards", json={"title": "a" * 101})
    assert response.status_code == 422


def test_create_card_title_at_max_length_is_created(client):
    response = client.post("/api/cards", json={"title": "a" * 100})
    assert response.status_code == 201


def test_create_card_description_too_long_is_422(client):
    response = client.post(
        "/api/cards", json={"title": "Valid title", "description": "a" * 1001}
    )
    assert response.status_code == 422


def test_create_card_description_at_max_length_is_created(client):
    response = client.post(
        "/api/cards", json={"title": "Valid title", "description": "a" * 1000}
    )
    assert response.status_code == 201


def test_create_card_new_card_is_always_todo(client):
    response = client.post(
        "/api/cards", json={"title": "Ignore status", "status": "done"}
    )
    assert response.status_code == 201
    assert response.json()["status"] == "todo"


# --- PATCH /api/cards/{id} -----------------------------------------------


def test_update_card_title_and_description(client):
    created = create_card(client, title="Old title", description="Old description").json()

    response = client.patch(
        f"/api/cards/{created['id']}",
        json={"title": "New title", "description": "New description"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["title"] == "New title"
    assert body["description"] == "New description"
    assert body["id"] == created["id"]


def test_update_card_partial_update_keeps_other_fields(client):
    created = create_card(client, title="Keep me", description="Change me").json()

    response = client.patch(
        f"/api/cards/{created['id']}", json={"description": "Changed"}
    )
    assert response.status_code == 200
    body = response.json()
    assert body["title"] == "Keep me"
    assert body["description"] == "Changed"


def test_update_card_status(client):
    created = create_card(client).json()

    response = client.patch(
        f"/api/cards/{created['id']}", json={"status": "in_progress"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "in_progress"

    response = client.patch(f"/api/cards/{created['id']}", json={"status": "done"})
    assert response.status_code == 200
    assert response.json()["status"] == "done"


def test_update_card_invalid_status_is_422(client):
    created = create_card(client).json()

    response = client.patch(
        f"/api/cards/{created['id']}", json={"status": "not_a_status"}
    )
    assert response.status_code == 422


def test_update_card_empty_title_is_422(client):
    created = create_card(client).json()

    response = client.patch(f"/api/cards/{created['id']}", json={"title": ""})
    assert response.status_code == 422


def test_update_card_title_too_long_is_422(client):
    created = create_card(client).json()

    response = client.patch(
        f"/api/cards/{created['id']}", json={"title": "a" * 101}
    )
    assert response.status_code == 422


def test_update_card_description_too_long_is_422(client):
    created = create_card(client).json()

    response = client.patch(
        f"/api/cards/{created['id']}", json={"description": "a" * 1001}
    )
    assert response.status_code == 422


def test_update_card_not_found_is_404(client):
    response = client.patch("/api/cards/999999", json={"title": "Doesn't matter"})
    assert response.status_code == 404


# --- DELETE /api/cards/{id} -----------------------------------------------


def test_delete_card(client):
    created = create_card(client).json()

    response = client.delete(f"/api/cards/{created['id']}")
    assert response.status_code == 204

    remaining = client.get("/api/cards").json()
    assert remaining == []


def test_delete_card_not_found_is_404(client):
    response = client.delete("/api/cards/999999")
    assert response.status_code == 404


def test_delete_card_twice_is_404_second_time(client):
    created = create_card(client).json()

    first = client.delete(f"/api/cards/{created['id']}")
    assert first.status_code == 204

    second = client.delete(f"/api/cards/{created['id']}")
    assert second.status_code == 404


# --- CORS -----------------------------------------------------------------


def test_cors_allows_frontend_origin(client):
    response = client.get(
        "/api/cards", headers={"Origin": "http://localhost:5173"}
    )
    assert response.headers["access-control-allow-origin"] == "http://localhost:5173"
