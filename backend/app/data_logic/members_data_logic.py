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
        members (list): A list of dictionaries, each representing a member.
    Raises:
        sqliteError: If there is an issue with the database connection or query execution.
    """
    try:
        conn = get_db_connection()
        members = conn.execute("SELECT * FROM Members;").fetchall()
        conn.close()
        return [dict(member) for member in members]
    except sqlite3.Error as sqliteError:
        raise sqlite3.Error(f"Database error: {sqliteError}")
    except Exception as e:
        raise Exception(f"Error: {e}")

def get_member(member_id: int):
    """
    Retrieve a specific member from the database by their ID.
    Connects to the database, executes a query to fetch the member with the given ID, and returns the result as a dictionary.
    Parameters:
        member_id (int): The ID of the member to retrieve.
    Returns:
        member (dict): A dictionary representing the member.
    Raises:
        sqliteError: If there is an issue with the database connection or query execution.
    """
    try:
        if(member_id <= 0):
            raise ValueError("Member ID must be a positive integer")

        conn = get_db_connection()
        member = conn.execute("SELECT * FROM Members WHERE id=?;", (member_id,)).fetchone()
        conn.close()

        if(not member):
            raise KeyError("Member not found")

        return dict(member)
    except sqlite3.Error as sqliteError:
        raise sqlite3.Error(f"Database error: {sqliteError}")
    except Exception as e:
        raise Exception(f"Error: {e}")

def get_member_by_name(member_name: str):
    """
    Retrieve a specific member from the database by its name.
    Connects to the database, executes a query to fetch the member with the given name, and returns the result as a dictionary.
    Parameters:
        member_name (str): The name of the member to retrieve.
    Returns:
        member (dict): A dictionary representing the member.
    Raises:
        ValueError: If the member name is empty.
        KeyError: If the member is not found.
        sqlite3.Error: If there is an issue with the database connection or query execution.
        Exception: If any other error occurs.
    """
    try:
        if(member_name == ""):
            raise ValueError("Member Name must be valid")

        conn = get_db_connection()
        member = conn.execute("SELECT * FROM Members WHERE name=?;", (member_name,)).fetchone()
        conn.close()
        
        if(not member):
            raise KeyError("Member not found")
        
        return dict(member)

    except sqlite3.Error as sqliteError:
        raise sqlite3.Error(f"Database error: {sqliteError}")
    except Exception as exception:
        raise Exception(f"Error: {exception}")

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
        raise sqlite3.Error(f"Database error: {sqliteError}")
    except sqlite3.IntegrityError:
        raise Exception("Integrity error: Possible duplicate or constraint violation")
    except Exception as e:
        raise Exception(f"Error: {e}")

def edit_member(member_id:int, member: Member):
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
        if(member_id <= 0):
            raise ValueError("member ID must be a positive integer")

        conn = get_db_connection()
        cursor = conn.cursor()
        member = conn.execute("SELECT * FROM Members WHERE id=?;", (member_id,)).fetchone()
        
        if(not member):
            raise KeyError("Member not found")
        
        cursor.execute("UPDATE Members SET name=?, email=?, phone=? WHERE id=?;", (member.name, member.email, member.phone, member.id))
        conn.commit()
        conn.close()
    except sqlite3.Error as sqliteError:
        raise sqlite3.Error(f"Database error: {sqliteError}")
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
        if(member_id <= 0):
            raise ValueError("Member ID must be a positive integer")

        conn = get_db_connection()
        cursor = conn.cursor()
        member = conn.execute("SELECT * FROM Members WHERE id=?;", (member_id,)).fetchone()
        
        if(not member):
            raise KeyError("Member not found")
        
        cursor.execute("DELETE FROM Members WHERE id=?;", (member_id,))
        
        conn.commit()
        conn.close()
    except sqlite3.Error as sqliteError:
        raise sqlite3.Error(f"Database error: {sqliteError}")
    except Exception as e:
        raise Exception(f"Error: {e}")
