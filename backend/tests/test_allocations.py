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

def test_get_allocations(test_db):
    """
    Test case for retrieving all allocations.
    This test verifies that the endpoint returns an empty list when there are no allocations.
    """
    response = client.get("/allocations/")
    assert response.status_code == 200
    assert response.json() == []

def test_add_allocation(test_db):
    """
    Test case for adding a new allocation.
    This test verifies that a new allocation can be successfully added to the database.
    """
    test_db.execute("INSERT INTO Books (name, author, total_copies) VALUES ('Test Book', 'Author', 5)")
    test_db.execute("INSERT INTO Members (name, email, phone) VALUES ('John Doe', 'john@example.com', '1234567890')")
    test_db.commit()
    
    allocation_data = {
        "id": 1,
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
    """
    Test case for retrieving an allocation by its ID.
    This test verifies that the endpoint returns the correct allocation details.
    """
    test_db.execute("INSERT INTO Allocations (book_id, member_id, start_date, end_date) VALUES (1, 1, '2024-03-01', '2024-03-10')")
    test_db.commit()
    
    response = client.get("/allocations/1")
    assert response.status_code == 200
    assert "id" in response.json()

def test_get_allocations_of_book(test_db):
    """
    Test case for retrieving allocations of a specific book.
    This test verifies that the endpoint returns the correct allocations for the given book.
    """
    test_db.execute("INSERT INTO Allocations (book_id, member_id, start_date, end_date) VALUES (1, 1, '2024-03-01', '2024-03-10')")
    test_db.commit()
    
    response = client.get("/allocations/?book=1")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_get_allocations_of_member(test_db):
    """
    Test case for retrieving allocations of a specific member.
    This test verifies that the endpoint returns the correct allocations for the given member.
    """
    test_db.execute("INSERT INTO Allocations (book_id, member_id, start_date, end_date) VALUES (1, 1, '2024-03-01', '2024-03-10')")
    test_db.commit()
    
    response = client.get("/allocations/?member=1")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_edit_allocation(test_db):
    """
    Test case for editing an existing allocation.
    This test verifies that an allocation can be successfully updated in the database.
    """
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
    """
    Test case for deleting an allocation.
    This test verifies that an allocation can be successfully deleted from the database.
    """
    test_db.execute("INSERT INTO Allocations (book_id, member_id, start_date, end_date) VALUES (1, 1, '2024-03-01', '2024-03-10')")
    test_db.commit()
    
    response = client.delete("/allocations/1")
    assert response.status_code == 200
    assert response.json() == {"msg": "Success"}

def test_get_nonexistent_allocation(test_db):
    """
    Test case for retrieving a nonexistent allocation.
    This test verifies that the endpoint returns a 404 status code for a nonexistent allocation.
    """
    response = client.get("/allocations/999")
    assert response.status_code == 404, response.text
    
def test_delete_nonexistent_allocation(test_db):
    """
    Test case for deleting a nonexistent allocation.
    This test verifies that the endpoint returns a 404 status code for a nonexistent allocation.
    """
    response = client.delete("/allocations/999")
    assert response.status_code == 404, response.text
    
def test_invalid_allocation_id(test_db):
    """
    Test case for retrieving an allocation with an invalid ID.
    This test verifies that the endpoint returns a 400 status code for an invalid allocation ID.
    """
    response = client.get("/allocations/abc")
    assert response.status_code == 400
