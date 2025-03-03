import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

# Test Cases

def test_get_all_books():
    response = client.get("/books/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_book():
    response = client.post("/books/", json={"name": "Test Book", "author": "Author", "total_copies": 5})
    assert response.status_code == 200
    
    response = client.get("/books/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Test Book"

def test_add_book():
    response = client.post("/books/", json={"name": "New Book", "author": "New Author", "total_copies": 3})
    assert response.status_code == 200
    assert response.json()["msg"] == "Success"

def test_edit_book():
    response = client.put("/books/1", json={"name": "Updated Book", "author": "Updated Author", "total_copies": 10, "allocated_copies": 0})
    assert response.status_code == 200
    assert response.json()["msg"] == "Success"

def test_get_nonexistent_book():
    response = client.get("/books/99")
    assert response.status_code == 404

def test_add_book_with_zero_copies():
    response = client.post("/books/", json={"name": "Zero Copies", "author": "Nobody", "total_copies": 0})
    assert response.status_code == 200

def test_get_book_with_invalid_id():
    response = client.get("/books/-1")
    assert response.status_code == 400

def test_delete_allocated_book():
    client.post("/books/", json={"name": "Allocated Book", "author": "Someone", "total_copies": 2})
    response = client.delete("/books/1")
    assert response.status_code == 400
