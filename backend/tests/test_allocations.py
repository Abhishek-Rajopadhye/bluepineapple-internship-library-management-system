import pytest
from fastapi.testclient import TestClient
from app import app
from app.database import get_db_connection
from app.models import Allocation
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

def test_get_allocations(test_db):
    response = client.get("/allocations/")
    assert response.status_code == 200
    assert response.json() == []

def test_add_allocation(test_db):
    test_db.execute("INSERT INTO Books (name, author, total_copies) VALUES ('Test Book', 'Author', 5)")
    test_db.execute("INSERT INTO Members (name, email, phone) VALUES ('John Doe', 'john@example.com', '1234567890')")
    test_db.commit()
    
    allocation_data = {
        "id":1,
        "book_id": 1,
        "member_id": 1,
        "start_date": "2024-03-01",
        "end_date": "2024-03-10",
        "returned": False,
        "overdue": False
    }
    
    response = client.post("/allocations/", json=allocation_data)
    assert response.status_code == 200
    assert response.json() == {"msg": "Success"}

def test_get_allocation_by_id(test_db):
    test_db.execute("INSERT INTO Allocations (book_id, member_id, start_date, end_date) VALUES (1, 1, '2024-03-01', '2024-03-10')")
    test_db.commit()
    
    response = client.get("/allocations/1")
    assert response.status_code == 200
    assert "id" in response.json()

def test_get_allocations_of_book(test_db):
    test_db.execute("INSERT INTO Allocations (book_id, member_id, start_date, end_date) VALUES (1, 1, '2024-03-01', '2024-03-10')")
    test_db.commit()
    
    response = client.get("/allocations/?book=1")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_get_allocations_of_member(test_db):
    test_db.execute("INSERT INTO Allocations (book_id, member_id, start_date, end_date) VALUES (1, 1, '2024-03-01', '2024-03-10')")
    test_db.commit()
    
    response = client.get("/allocations/?member=1")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_edit_allocation(test_db):
    test_db.execute(
        "INSERT INTO Allocations (book_id, member_id, start_date, end_date, returned, overdue) VALUES (1, 1, '2024-03-01', '2024-03-10', 0, 0)"
    )
    test_db.commit()
    
    updated_data = {
        "id": 1,
        "book_id": 1,
        "member_id": 1,
        "start_date": "2024-03-02",
        "end_date": "2024-03-12",
        "returned": True,
        "overdue": False
    }
    response = client.put("/allocations/1", json=updated_data)
    assert response.status_code == 200, response.text
    assert response.json() == {"msg": "Success"}

def test_delete_allocation(test_db):
    test_db.execute("INSERT INTO Allocations (book_id, member_id, start_date, end_date) VALUES (1, 1, '2024-03-01', '2024-03-10')")
    test_db.commit()
    
    response = client.delete("/allocations/1")
    assert response.status_code == 200
    assert response.json() == {"msg": "Success"}

def test_get_nonexistent_allocation(test_db):
    response = client.get("/allocations/999")
    assert response.status_code == 404, response.text
    
def test_delete_nonexistent_allocation(test_db):
    response = client.delete("/allocations/999")
    assert response.status_code == 404, response.text
    
def test_invalid_allocation_id(test_db):
    response = client.get("/allocations/abc")
    assert response.status_code == 400
    