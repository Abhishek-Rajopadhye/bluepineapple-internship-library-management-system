import pytest
from fastapi.testclient import TestClient
from app import app
from app.database import get_db_connection
import sqlite3

client = TestClient(app)

def override_get_db_connection():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.executescript("""
        CREATE TABLE Books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            author TEXT NOT NULL,
            total_copies INTEGER NOT NULL,
            allocated_copies INTEGER DEFAULT 0
        );
    """)
    conn.commit()
    return conn

app.dependency_overrides[get_db_connection] = override_get_db_connection

@pytest.fixture(scope="function")
def test_db():
    conn = override_get_db_connection()
    yield conn
    conn.close()

def test_get_books(test_db):
    response = client.get("/books/")
    assert response.status_code == 200
    assert response.json() == []

def test_add_book(test_db):
    book_data = {
        "id":0,
        "name": "Test Book",
        "author": "Author Name",
        "total_copies": 5,
        "allocated_copies": 0
    }
    response = client.post("/books/", json=book_data)
    assert response.status_code == 200
    assert response.json() == {"msg": "Success"}

def test_get_book_by_id(test_db):
    test_db.execute("INSERT INTO Books (name, author, total_copies) VALUES ('Test Book', 'Author Name', 5)")
    test_db.commit()
    
    response = client.get("/books/1")
    assert response.status_code == 200
    assert "id" in response.json()

def test_get_book_by_name(test_db):
    test_db.execute("INSERT INTO Books (name, author, total_copies) VALUES ('Unique Book', 'Author', 5)")
    test_db.commit()
    
    response = client.get("/books/name=Unique%20Book")
    assert response.status_code == 200
    assert response.json()["name"] == "Unique Book"

def test_edit_book(test_db):
    test_db.execute("INSERT INTO Books (name, author, total_copies) VALUES ('Old Book', 'Old Author', 2)")
    test_db.commit()
    
    updated_data = {
        "name": "Updated Book",
        "author": "New Author",
        "total_copies": 10,
        "allocated_copies": 0
    }
    response = client.put("/books/1", json=updated_data)
    assert response.status_code == 200
    assert response.json() == {"msg": "Success"}

def test_delete_book(test_db):
    test_db.execute("INSERT INTO Books (name, author, total_copies) VALUES ('Book to Delete', 'Author', 1)")
    test_db.commit()
    
    response = client.delete("/books/1")
    assert response.status_code == 200
    assert response.json() == {"msg": "Success"}

def test_get_nonexistent_book(test_db):
    response = client.get("/books/999")
    assert response.status_code == 404

def test_delete_nonexistent_book(test_db):
    response = client.delete("/books/999")
    assert response.status_code == 404

def test_invalid_book_id(test_db):
    response = client.get("/books/abc")
    assert response.status_code == 400
