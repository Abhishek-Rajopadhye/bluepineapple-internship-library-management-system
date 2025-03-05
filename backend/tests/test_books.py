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


def test_get_books(test_db):
    """
    Test case for retrieving all books.
    This test verifies that the endpoint returns an empty list when there are no books.
    """
    response = client.get("/books/")
    assert response.status_code == 200
    assert response.json() == []

def test_add_book(test_db):
    """
    Test case for adding a new book.
    This test verifies that a new book can be successfully added to the database.
    """
    book_data = {
        "id": 0,
        "name": "Test Book",
        "author": "Author Name",
        "total_copies": 5,
        "allocated_copies": 0
    }
    response = client.post("/books/", json=book_data)
    assert response.status_code == 200
    assert response.json() == {"msg": "Success"}

def test_get_book_by_id(test_db):
    """
    Test case for retrieving a book by its ID.
    This test verifies that the endpoint returns the correct book details.
    """
    test_db.execute("INSERT INTO Books (name, author, total_copies) VALUES ('Test Book', 'Author Name', 5)")
    test_db.commit()
    
    response = client.get("/books/1")
    assert response.status_code == 200
    assert "id" in response.json()

def test_get_book_by_name(test_db):
    """
    Test case for retrieving a book by its name.
    This test verifies that the endpoint returns the correct book details.
    """
    test_db.execute("INSERT INTO Books (name, author, total_copies) VALUES ('Test Book', 'Author Name', 5)")
    test_db.commit()
    
    response = client.get("/books/?name=Test%20Book")
    assert response.status_code == 200
    assert response.json()[0]["name"] == "Test Book"

def test_edit_book(test_db):
    """
    Test case for editing an existing book.
    This test verifies that a book can be successfully updated in the database.
    """
    test_db.execute("INSERT INTO Books (name, author, total_copies) VALUES ('Old Book', 'Old Author', 2)")
    test_db.commit()
    
    updated_data = {
        "id": 1,
        "name": "Updated Book",
        "author": "New Author",
        "total_copies": 10,
        "allocated_copies": 0
    }
    response = client.put("/books/1", json=updated_data)
    assert response.status_code == 200
    assert response.json() == {"msg": "Success"}

def test_delete_book(test_db):
    """
    Test case for deleting a book.
    This test verifies that a book can be successfully deleted from the database.
    """
    test_db.execute("INSERT INTO Books (name, author, total_copies) VALUES ('Book to Delete', 'Author', 1)")
    test_db.commit()
    
    response = client.delete("/books/1")
    assert response.status_code == 200
    assert response.json() == {"msg": "Success"}

def test_get_nonexistent_book(test_db):
    """
    Test case for retrieving a nonexistent book.
    This test verifies that the endpoint returns a 404 status code for a nonexistent book.
    """
    response = client.get("/books/999")
    assert response.status_code == 404

def test_delete_nonexistent_book(test_db):
    """
    Test case for deleting a nonexistent book.
    This test verifies that the endpoint returns a 404 status code for a nonexistent book.
    """
    response = client.delete("/books/999")
    assert response.status_code == 404

def test_invalid_book_id(test_db):
    """
    Test case for retrieving a book with an invalid ID.
    This test verifies that the endpoint returns a 400 status code for an invalid book ID.
    """
    response = client.get("/books/abc")
    assert response.status_code == 400