import pytest
import sqlite3
from app.data_logic.members_data_logic import add_member, get_member, get_all_members, edit_member, delete_member
from app.models import Member
from app.database import get_db_connection

# Create an in-memory SQLite database for testing
def get_test_db_connection():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Create the Members table
    cursor.execute('''
    CREATE TABLE Members (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE,
        phone TEXT
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

def test_add_member(test_db):
    member = Member(id=1, name="John Doe", email="john@example.com", phone="1234567890")
    add_member(member)
    result = get_member(1)
    assert result["name"] == "John Doe"

def test_get_member(test_db):
    member = Member(id=1, name="Alice", email="alice@example.com", phone="9876543210")
    add_member(member)
    retrieved = get_member(1)
    assert retrieved["email"] == "alice@example.com"

def test_get_all_members(test_db):
    member1 = Member(id=1, name="Member One", email="one@example.com", phone="1111111111")
    member2 = Member(id=2, name="Member Two", email="two@example.com", phone="2222222222")
    add_member(member1)
    add_member(member2)
    members = get_all_members()
    assert len(members) == 2

def test_edit_member(test_db):
    member = Member(id=1, name="Old Name", email="old@example.com", phone="9999999999")
    add_member(member)
    updated_member = Member(id=1, name="New Name", email="new@example.com", phone="8888888888")
    edit_member(1, updated_member)
    edited = get_member(1)
    assert edited["name"] == "New Name"

def test_get_nonexistent_member(test_db):
    with pytest.raises(KeyError):
        get_member(99)

def test_add_member_without_email(test_db):
    member = Member(id=1, name="No Email", email=None, phone="7777777777")
    add_member(member)
    result = get_member(1)
    assert result["email"] is None

def test_get_member_with_negative_id(test_db):
    with pytest.raises(ValueError):
        get_member(-1)

def test_delete_member_with_active_allocations(test_db, monkeypatch):
    member = Member(id=1, name="Active Allocations", email="active@example.com", phone="6666666666")
    add_member(member)
    monkeypatch.setattr("app.members_data_logic.get_allocations_of_member", lambda _: ["mock_allocation"])
    with pytest.raises(Exception, match="Member has active allocations and cannot be deleted"):
        delete_member(1)
