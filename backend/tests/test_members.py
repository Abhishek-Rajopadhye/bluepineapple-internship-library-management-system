import pytest
from fastapi.testclient import TestClient
from app import app
from app.database import get_db_connection
import sqlite3

client = TestClient(app)

def override_get_db_connection():
    """
    Override the database connection to use an in-memory SQLite database for testing.
    This function creates the necessary tables and returns the connection.
    """
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
        CREATE TABLE History (
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
    """
    Pytest fixture to provide a temporary in-memory database for testing.
    This fixture sets up the database before each test and tears it down after each test.
    """
    conn = override_get_db_connection()
    yield conn
    conn.close()

def test_get_members(test_db):
    """
    Test case for retrieving all members.
    This test verifies that the endpoint returns an empty list when there are no members.
    """
    response = client.get("/members/")
    assert response.status_code == 200
    assert response.json() == []

def test_add_member(test_db):
    """
    Test case for adding a new member.
    This test verifies that a new member can be successfully added to the database.
    """
    member_data = {
        "id": 0,
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "1234567890"
    }
    response = client.post("/members/", json=member_data)
    assert response.status_code == 200
    assert response.json() == {"msg": "Success"}

def test_get_member_by_id(test_db):
    """
    Test case for retrieving a member by its ID.
    This test verifies that the endpoint returns the correct member details.
    """
    test_db.execute("INSERT INTO Members (name, email, phone) VALUES ('John Doe', 'john@example.com', '1234567890')")
    test_db.commit()
    
    response = client.get("/members/1")
    assert response.status_code == 200
    assert "id" in response.json()

def test_get_member_by_name(test_db):
    """
    Test case for retrieving a member by its name.
    This test verifies that the endpoint returns the correct member details.
    """
    test_db.execute("INSERT INTO Members (name, email, phone) VALUES ('John Doe', 'john@example.com', '1234567890')")
    test_db.commit()
    
    response = client.get("/members/?name=John%20Doe")
    assert response.status_code == 200
    
    json_response = response.json()
    if isinstance(json_response, list):
        json_response = json_response[0]
    
    assert json_response["name"] == "John Doe"
    assert json_response["email"] == "john@example.com"
    assert json_response["phone"] == "1234567890"

def test_edit_member(test_db):
    """
    Test case for editing an existing member.
    This test verifies that a member can be successfully updated in the database.
    """
    test_db.execute("INSERT INTO Members (name, email, phone) VALUES ('Old Name', 'old@example.com', '1111111111')")
    test_db.commit()
    
    updated_data = {
        "id": 1,
        "name": "New Name",
        "email": "new@example.com",
        "phone": "2222222222"
    }
    response = client.put("/members/1", json=updated_data)
    assert response.status_code == 200
    assert response.json() == {"msg": "Success"}

def test_delete_member(test_db):
    """
    Test case for deleting a member.
    This test verifies that a member can be successfully deleted from the database.
    """
    test_db.execute("INSERT INTO Members (name, email, phone) VALUES ('Delete Me', 'delete@example.com', '3333333333')")
    test_db.commit()
    
    response = client.delete("/members/1")
    assert response.status_code == 200
    assert response.json() == {"msg": "Success"}

def test_get_nonexistent_member(test_db):
    """
    Test case for retrieving a nonexistent member.
    This test verifies that the endpoint returns a 404 status code for a nonexistent member.
    """
    response = client.get("/members/999")
    assert response.status_code == 404

def test_delete_nonexistent_member(test_db):
    """
    Test case for deleting a nonexistent member.
    This test verifies that the endpoint returns a 404 status code for a nonexistent member.
    """
    response = client.delete("/members/999")
    assert response.status_code == 404

def test_invalid_member_id(test_db):
    """
    Test case for retrieving a member with an invalid ID.
    This test verifies that the endpoint returns a 400 status code for an invalid member ID.
    """
    response = client.get("/members/abc")
    assert response.status_code == 400