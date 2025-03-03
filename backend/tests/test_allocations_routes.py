import pytest
from fastapi.testclient import TestClient
from app import app
from datetime import date

client = TestClient(app)

# Test Cases

def test_get_all_allocations():
    response = client.get("/allocations/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_allocation():
    response = client.post("/allocations/", json={"book_id": 1, "member_id": 1, "start_date": str(date.today()), "end_date": str(date.today()), "returned": False, "overdue": False})
    assert response.status_code == 200
    
    response = client.get("/allocations/1")
    assert response.status_code == 200
    assert response.json()["book_id"] == 1

def test_add_allocation():
    response = client.post("/allocations/", json={"book_id": 2, "member_id": 2, "start_date": str(date.today()), "end_date": str(date.today()), "returned": False, "overdue": False})
    assert response.status_code == 200
    assert response.json()["msg"] == "Success"

def test_edit_allocation():
    response = client.put("/allocations/1", json={"book_id": 1, "member_id": 1, "start_date": str(date.today()), "end_date": str(date.today()), "returned": True, "overdue": False})
    assert response.status_code == 200
    assert response.json()["msg"] == "Success"

def test_get_nonexistent_allocation():
    response = client.get("/allocations/99")
    assert response.status_code == 404

def test_add_overdue_allocation():
    response = client.post("/allocations/", json={"book_id": 3, "member_id": 3, "start_date": str(date.today()), "end_date": str(date.today()), "returned": False, "overdue": True})
    assert response.status_code == 200

def test_get_allocation_with_invalid_id():
    response = client.get("/allocations/-1")
    assert response.status_code == 400

def test_delete_nonexistent_allocation():
    response = client.delete("/allocations/99")
    assert response.status_code == 404