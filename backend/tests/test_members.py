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
        CREATE TABLE Members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE,
            phone TEXT
        );
        CREATE TABLE Allocations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER NOT NULL,
            member_id INTEGER NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            returned BOOLEAN DEFAULT FALSE,
            overdue BOOLEAN DEFAULT FALSE,
            FOREIGN KEY (book_id) REFERENCES Books(id),
            FOREIGN KEY (member_id) REFERENCES Members(id)
        );
    """)
    conn.commit()
    return conn

app.dependency_overrides = {get_db_connection: override_get_db_connection}


@pytest.fixture(scope="function")
def test_db():
    conn = override_get_db_connection()
    yield conn
    conn.close()

def test_get_members(test_db):
    response = client.get("/members/")
    assert response.status_code == 200
    assert response.json() == []

def test_add_member(test_db):
    member_data = {
        "id":0,
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "1234567890"
    }
    response = client.post("/members/", json=member_data)
    assert response.status_code == 200
    assert response.json() == {"msg": "Success"}

def test_get_member_by_id(test_db):
    test_db.execute("INSERT INTO Members (name, email, phone) VALUES ('John Doe', 'john@example.com', '1234567890')")
    test_db.commit()
    
    response = client.get("/members/1")
    assert response.status_code == 200
    assert "id" in response.json()

def test_get_member_by_name(test_db):
    test_db.execute("INSERT INTO Members (name, email, phone) VALUES ('John Doe', 'john@example.com', '1234567890')")
    test_db.commit()
    
    response = client.get("/members/?name=John%20Doe")
    assert response.status_code == 200
    
    json_response = response.json()
    if isinstance(json_response, list):
        json_response = json_response[0]
    print(json_response)
    
    assert json_response["name"] == "John Doe"
    assert json_response["email"] == "john@example.com"
    assert json_response["phone"] == "1234567890"

def test_edit_member(test_db):
    test_db.execute("INSERT INTO Members (name, email, phone) VALUES ('Old Name', 'old@example.com', '1111111111')")
    test_db.commit()
    
    updated_data = {
        "id":1,
        "name": "New Name",
        "email": "new@example.com",
        "phone": "2222222222"
    }
    response = client.put("/members/1", json=updated_data)
    assert response.status_code == 200
    assert response.json() == {"msg": "Success"}

def test_delete_member(test_db):
    test_db.execute("INSERT INTO Members (name, email, phone) VALUES ('Delete Me', 'delete@example.com', '3333333333')")
    test_db.commit()
    
    response = client.delete("/members/1")
    assert response.status_code == 200
    assert response.json() == {"msg": "Success"}

def test_get_nonexistent_member(test_db):
    response = client.get("/members/999")
    assert response.status_code == 404

def test_delete_nonexistent_member(test_db):
    response = client.delete("/members/999")
    assert response.status_code == 404

def test_invalid_member_id(test_db):
    response = client.get("/members/abc")
    assert response.status_code == 400
