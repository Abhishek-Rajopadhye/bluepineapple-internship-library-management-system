import pytest
import sqlite3
from app.data_logic.books_data_logic import add_book, get_book, get_all_books, edit_book, delete_book
from app.models import Book
from app.database import get_db_connection

# Create an in-memory SQLite database for testing
def get_test_db_connection():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Create the Books table
    cursor.execute('''
    CREATE TABLE Books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        author TEXT NOT NULL,
        total_copies INTEGER NOT NULL,
        allocated_copies INTEGER DEFAULT 0
    );
    ''')
    conn.commit()
    return conn

# Fixture to override database connection
@pytest.fixture(scope="function")
def test_db(monkeypatch):
    conn = get_test_db_connection()
    monkeypatch.setattr("app.database.get_db_connection", lambda: conn)
    yield conn
    conn.close()

# Test Cases

def test_add_book(test_db):
    book = Book(id=1, name="Test Book", author="Author", total_copies=5, allocated_copies=0)
    add_book(book)
    result = get_book(1)
    assert result["name"] == "Test Book"

def test_get_book(test_db):
    book = Book(id=1, name="Sample Book", author="Writer", total_copies=3, allocated_copies=0)
    add_book(book)
    retrieved = get_book(1)
    assert retrieved["author"] == "Writer"

def test_get_all_books(test_db):
    book1 = Book(id=1, name="Book One", author="Author1", total_copies=2, allocated_copies=0)
    book2 = Book(id=2, name="Book Two", author="Author2", total_copies=4, allocated_copies=0)
    add_book(book1)
    add_book(book2)
    books = get_all_books()
    assert len(books) == 2

def test_edit_book(test_db):
    book = Book(id=1, name="Old Title", author="Old Author", total_copies=3, allocated_copies=0)
    add_book(book)
    updated_book = Book(id=1, name="New Title", author="New Author", total_copies=5, allocated_copies=0)
    edit_book(1, updated_book)
    edited = get_book(1)
    assert edited["name"] == "New Title"

def test_get_nonexistent_book(test_db):
    with pytest.raises(KeyError):
        get_book(99)

def test_add_book_with_zero_copies(test_db):
    book = Book(id=1, name="Empty Book", author="Nobody", total_copies=0, allocated_copies=0)
    add_book(book)
    result = get_book(1)
    assert result["total_copies"] == 0

def test_get_book_with_negative_id(test_db):
    with pytest.raises(ValueError):
        get_book(-1)

def test_delete_allocated_book(test_db):
    book = Book(id=1, name="Allocated Book", author="Someone", total_copies=2, allocated_copies=1)
    add_book(book)
    with pytest.raises(Exception, match="Cannot delete a book that has been allocated"):
        delete_book(1)

# Additional rigorous test cases
def test_add_book_with_long_name(test_db):
    long_name = "A" * 256  # Exceeding typical length limits
    book = Book(id=1, name=long_name, author="Author", total_copies=1, allocated_copies=0)
    add_book(book)
    result = get_book(1)
    assert result["name"] == long_name

def test_add_book_with_empty_name(test_db):
    with pytest.raises(ValueError):
        book = Book(id=1, name="", author="Author", total_copies=1, allocated_copies=0)
        add_book(book)

def test_add_duplicate_books(test_db):
    book1 = Book(id=1, name="Duplicate Book", author="Same Author", total_copies=2, allocated_copies=0)
    book2 = Book(id=2, name="Duplicate Book", author="Same Author", total_copies=3, allocated_copies=0)
    add_book(book1)
    add_book(book2)
    books = get_all_books()
    assert len(books) == 2  # Different IDs but same name

def test_delete_nonexistent_book(test_db):
    with pytest.raises(KeyError):
        delete_book(99)

def test_edit_book_to_invalid_values(test_db):
    book = Book(id=1, name="Valid Book", author="Author", total_copies=2, allocated_copies=0)
    add_book(book)
    with pytest.raises(ValueError):
        updated_book = Book(id=1, name="", author="", total_copies=-5, allocated_copies=0)
        edit_book(1, updated_book)

def test_add_book_with_large_copies(test_db):
    book = Book(id=1, name="Big Library", author="Collector", total_copies=1000000, allocated_copies=0)
    add_book(book)
    result = get_book(1)
    assert result["total_copies"] == 1000000

def test_get_book_by_invalid_name(test_db):
    with pytest.raises(KeyError):
        get_book("Nonexistent Book")
