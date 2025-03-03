import pytest
import sqlite3
from app.database import get_db_connection, init_db

# Fixture for setting up a test database
@pytest.fixture(scope="function")
def test_db():
    conn = sqlite3.connect(":memory:")  # In-memory database for testing
    conn.row_factory = sqlite3.Row
    init_db()  # Create tables
    yield conn
    conn.close()

# Test Cases

def test_insert_and_retrieve_book(test_db):
    cursor = test_db.cursor()
    cursor.execute("INSERT INTO Books (name, author, total_copies) VALUES (?, ?, ?)", ("Test Book", "Author", 5))
    test_db.commit()
    result = cursor.execute("SELECT * FROM Books WHERE name=?", ("Test Book",)).fetchone()
    assert result["author"] == "Author"

def test_update_book(test_db):
    cursor = test_db.cursor()
    cursor.execute("INSERT INTO Books (name, author, total_copies) VALUES (?, ?, ?)", ("Old Book", "Old Author", 3))
    test_db.commit()
    cursor.execute("UPDATE Books SET name=? WHERE name=?", ("New Book", "Old Book"))
    test_db.commit()
    result = cursor.execute("SELECT * FROM Books WHERE name=?", ("New Book",)).fetchone()
    assert result is not None

def test_fetch_multiple_members(test_db):
    cursor = test_db.cursor()
    cursor.execute("INSERT INTO Members (name, email, phone) VALUES (?, ?, ?)", ("Member1", "m1@example.com", "123"))
    cursor.execute("INSERT INTO Members (name, email, phone) VALUES (?, ?, ?)", ("Member2", "m2@example.com", "456"))
    test_db.commit()
    members = cursor.execute("SELECT * FROM Members").fetchall()
    assert len(members) == 2

def test_foreign_key_constraint(test_db):
    cursor = test_db.cursor()
    with pytest.raises(sqlite3.IntegrityError):
        cursor.execute("INSERT INTO Allocations (book_id, member_id, start_date, end_date) VALUES (?, ?, ?, ?)", (99, 99, "2023-01-01", "2023-02-01"))

def test_insert_duplicate_member(test_db):
    cursor = test_db.cursor()
    cursor.execute("INSERT INTO Members (name, email, phone) VALUES (?, ?, ?)", ("John Doe", "john@example.com", "1234567890"))
    test_db.commit()
    with pytest.raises(sqlite3.IntegrityError):
        cursor.execute("INSERT INTO Members (name, email, phone) VALUES (?, ?, ?)", ("John Doe", "john@example.com", "0987654321"))

def test_null_optional_fields(test_db):
    cursor = test_db.cursor()
    cursor.execute("INSERT INTO Members (name, email, phone) VALUES (?, ?, ?)", ("No Email", None, "1111111111"))
    test_db.commit()
    result = cursor.execute("SELECT * FROM Members WHERE name=?", ("No Email",)).fetchone()
    assert result["email"] is None

def test_delete_member_with_allocations(test_db):
    cursor = test_db.cursor()
    cursor.execute("INSERT INTO Books (name, author, total_copies) VALUES (?, ?, ?)", ("Test Book", "Author", 5))
    cursor.execute("INSERT INTO Members (name, email, phone) VALUES (?, ?, ?)", ("John Doe", "john@example.com", "1234567890"))
    cursor.execute("INSERT INTO Allocations (book_id, member_id, start_date, end_date) VALUES (?, ?, ?, ?)", (1, 1, "2023-01-01", "2023-02-01"))
    test_db.commit()
    with pytest.raises(sqlite3.IntegrityError):
        cursor.execute("DELETE FROM Members WHERE id=?", (1,))
