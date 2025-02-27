from app.database import get_db_connection
from app.models import Member
import sqlite3

def get_all_members():
    """
    Retrieve all members from the database.
    Connects to the database, executes a query to fetch all members, and returns the results as a list of dictionaries.
    Parameters:
        None
    Returns:
        list: A list of dictionaries, each representing a member.
    Raises:
        sqliteError: If there is an issue with the database connection or query execution.
    """
    try:
        conn = get_db_connection()
        members = conn.execute("SELECT * FROM Members;").fetchall()
        conn.close()
        return [dict(member) for member in members]
    except sqlite3.Error as sqliteError:
        raise Exception(f"Database error: {sqliteError}")
    except Exception as e:
        raise Exception(f"Error: {e}")

def get_member(member_id: int):
    """
    Retrieve a specific member from the database by their ID.
    Connects to the database, executes a query to fetch the member with the given ID, and returns the result as a dictionary.
    Parameters:
        member_id (int): The ID of the member to retrieve.
    Returns:
        dict: A dictionary representing the member.
    Raises:
        sqliteError: If there is an issue with the database connection or query execution.
    """
    try:
        conn = get_db_connection()
        member = conn.execute("SELECT * FROM Members WHERE id=?;", (member_id,)).fetchone()
        conn.close()
        return dict(member)
    except sqlite3.Error as sqliteError:
        raise Exception(f"Database error: {sqliteError}")
    except Exception as e:
        raise Exception(f"Error: {e}")

def add_member(member: Member):
    """
    Add a new member to the database.
    Connects to the database, executes an insert query to add the member's details, and commits the transaction.
    Parameters:
        member (Member): An instance of the Member class containing the member's details.
    Returns:
        None
    Raises:
        sqliteError: If there is an issue with the database connection or query execution.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Members (name, email, phone) VALUES (?, ?, ?);", (member.name, member.email, member.phone))
        conn.commit()
        conn.close()
    except sqlite3.Error as sqliteError:
        raise Exception(f"Database error: {sqliteError}")
    except Exception as e:
        raise Exception(f"Error: {e}")

def edit_member(member: Member):
    """
    Edit an existing member's details in the database.
    Connects to the database, executes an update query to modify the member's details, and commits the transaction.
    Parameters:
        member (Member): An instance of the Member class containing the updated member's details.
    Returns:
        None
    Raises:
        sqliteError: If there is an issue with the database connection or query execution.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE Members SET name=?, email=?, phone=? WHERE id=?;", (member.name, member.email, member.phone, member.id))
        conn.commit()
        conn.close()
    except sqlite3.Error as sqliteError:
        raise Exception(f"Database error: {sqliteError}")
    except Exception as e:
        raise Exception(f"Error: {e}")

def delete_member(member_id: int):
    """
    Delete a member from the database by their ID.
    Connects to the database, executes a delete query to remove the member with the given ID, and commits the transaction.
    Parameters:
        member_id (int): The ID of the member to delete.
    Returns:
        None
    Raises:
        sqliteError: If there is an issue with the database connection or query execution.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Members WHERE id=?;", (member_id,))
        conn.commit()
        conn.close()
    except sqlite3.Error as sqliteError:
        raise Exception(f"Database error: {sqliteError}")
    except Exception as e:
        raise Exception(f"Error: {e}")
