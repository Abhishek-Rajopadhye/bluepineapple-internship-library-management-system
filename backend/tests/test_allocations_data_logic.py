import pytest
import sqlite3
from app.data_logic.allocations_data_logic import add_allocation, get_allocation, get_all_allocation, edit_allocation, delete_allocation
from app.models import Allocation
from app.database import get_db_connection
from datetime import date

# Create an in-memory SQLite database for testing
def get_test_db_connection():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Create the Allocations table
    cursor.execute('''
    CREATE TABLE Allocations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        book_id INTEGER NOT NULL,
        member_id INTEGER NOT NULL,
        start_date TEXT NOT NULL,
        end_date TEXT NOT NULL,
        returned BOOLEAN DEFAULT FALSE,
        overdue BOOLEAN DEFAULT FALSE
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

def test_add_allocation(test_db):
    allocation = Allocation(id=1, book_id=1, member_id=1, start_date=date.today(), end_date=date.today(), returned=False, overdue=False)
    add_allocation(allocation)
    result = get_allocation(1)
    assert result["book_id"] == 1

def test_get_allocation(test_db):
    allocation = Allocation(id=1, book_id=2, member_id=3, start_date=date.today(), end_date=date.today(), returned=False, overdue=False)
    add_allocation(allocation)
    retrieved = get_allocation(1)
    assert retrieved["member_id"] == 3

def test_get_all_allocations(test_db):
    allocation1 = Allocation(id=1, book_id=1, member_id=1, start_date=date.today(), end_date=date.today(), returned=False, overdue=False)
    allocation2 = Allocation(id=2, book_id=2, member_id=2, start_date=date.today(), end_date=date.today(), returned=False, overdue=False)
    add_allocation(allocation1)
    add_allocation(allocation2)
    allocations = get_all_allocation()
    assert len(allocations) == 2

def test_edit_allocation(test_db):
    allocation = Allocation(id=1, book_id=1, member_id=1, start_date=date.today(), end_date=date.today(), returned=False, overdue=False)
    add_allocation(allocation)
    updated_allocation = Allocation(id=1, book_id=2, member_id=2, start_date=date.today(), end_date=date.today(), returned=True, overdue=False)
    edit_allocation(1, updated_allocation)
    edited = get_allocation(1)
    assert edited["returned"] is True

def test_get_nonexistent_allocation(test_db):
    with pytest.raises(KeyError):
        get_allocation(99)

def test_add_overdue_allocation(test_db):
    allocation = Allocation(id=1, book_id=1, member_id=1, start_date=date.today(), end_date=date.today(), returned=False, overdue=True)
    add_allocation(allocation)
    result = get_allocation(1)
    assert result["overdue"] is True

def test_get_allocation_with_negative_id(test_db):
    with pytest.raises(ValueError):
        get_allocation(-1)

def test_delete_nonexistent_allocation(test_db):
    with pytest.raises(KeyError):
        delete_allocation(99)
