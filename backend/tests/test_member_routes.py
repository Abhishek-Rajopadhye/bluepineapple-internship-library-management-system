import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

# Test Cases

def test_get_all_members():
    response = client.get("/members/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_member():
    response = client.post("/members/", json={"name": "John Doe", "email": "john@example.com", "phone": "1234567890"})
    assert response.status_code == 200
    
    response = client.get("/members/1")
    assert response.status_code == 200
    assert response.json()["name"] == "John Doe"

def test_add_member():
    response = client.post("/members/", json={"name": "Jane Doe", "email": "jane@example.com", "phone": "0987654321"})
    assert response.status_code == 200
    assert response.json()["msg"] == "Success"

def test_edit_member():
    response = client.put("/members/1", json={"name": "Updated Name", "email": "updated@example.com", "phone": "5555555555"})
    assert response.status_code == 200
    assert response.json()["msg"] == "Success"

def test_get_nonexistent_member():
    response = client.get("/members/99")
    assert response.status_code == 404

def test_add_member_without_email():
    response = client.post("/members/", json={"name": "No Email", "email": None, "phone": "7777777777"})
    assert response.status_code == 200

def test_get_member_with_invalid_id():
    response = client.get("/members/-1")
    assert response.status_code == 400

def test_delete_member_with_active_allocations():
    client.post("/members/", json={"name": "Active Allocations", "email": "active@example.com", "phone": "6666666666"})
    response = client.delete("/members/1")
    assert response.status_code == 400
