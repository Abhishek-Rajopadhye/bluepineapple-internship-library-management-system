from app.database import get_db_connection
from app.models import Allocation
import sqlite3

def get_all_allocation():
    """
    Retrieve all allocations from the database.
    Connects to the database, executes a query to fetch all allocations, and returns the results as a list of dictionaries.
    Parameters:
        None
    Returns:
        list: A list of dictionaries, each representing an allocation.
    Raises:
        sqliteError: If there is an issue with the database connection or query execution.
        exception: If any other error occurs
    """
    try:
        conn = get_db_connection()
        allocations = conn.execute("SELECT * FROM Allocations;").fetchall()
        conn.close()
        return [dict(allocation) for allocation in allocations]
    except sqlite3.Error as sqliteError:
        raise Exception(f"Database error: {sqliteError}")
    except Exception as exception:
        raise Exception(f"Error: {exception}")

def get_allocation(allocation_id: int):
    """
    Retrieve a specific allocation from the database by its ID.
    Connects to the database, executes a query to fetch the allocation with the given ID, and returns the result as a dictionary.
    Parameters:
        allocation_id (int): The ID of the allocation to retrieve.
    Returns:
        dict: A dictionary representing the allocation.
    Raises:
        sqliteError: If there is an issue with the database connection or query execution.
        exception: If any other error occurs
    """
    try:
        conn = get_db_connection()
        allocation = conn.execute("SELECT * FROM Allocations WHERE id=?;", (allocation_id,)).fetchone()
        conn.close()
        return dict(allocation)
    except sqlite3.Error as sqliteError:
        raise Exception(f"Database error: {sqliteError}")
    except Exception as exception:
        raise Exception(f"Error: {exception}")

def get_allocations_of_book(book_id: int):
    """
    Retrieve all allocations for a specific book from the database.
    Connects to the database, executes a query to fetch all allocations for the given book ID, and returns the results as a list of dictionaries.
    Parameters:
        book_id (int): The ID of the book to retrieve allocations for.
    Returns:
        list: A list of dictionaries, each representing an allocation.
    Raises:
        sqliteError: If there is an issue with the database connection or query execution.
        exception: If any other error occurs
    """
    try:
        conn = get_db_connection()
        allocations = conn.execute("SELECT * FROM Allocations WHERE book_id=?;", (book_id,)).fetchall()
        conn.close()
        return [dict(allocation) for allocation in allocations]
    except sqlite3.Error as sqliteError:
        raise Exception(f"Database error: {sqliteError}")
    except Exception as exception:
        raise Exception(f"Error: {exception}")

def get_allocations_of_member(member_id: int):
    """
    Retrieve all allocations for a specific member from the database.
    Connects to the database, executes a query to fetch all allocations for the given member ID, and returns the results as a list of dictionaries.
    Parameters:
        member_id (int): The ID of the member to retrieve allocations for.
    Returns:
        list: A list of dictionaries, each representing an allocation.
    Raises:
        sqliteError: If there is an issue with the database connection or query execution.
        exception: If any other error occurs
    """
    try:
        conn = get_db_connection()
        allocations = conn.execute("SELECT * FROM Allocations WHERE member_id=?;", (member_id,)).fetchall()
        conn.close()
        return [dict(allocation) for allocation in allocations]
    except sqlite3.Error as sqliteError:
        raise Exception(f"Database error: {sqliteError}")
    except Exception as exception:
        raise Exception(f"Error: {exception}")

def get_allocation_of_book_of_member(book_id: int, member_id: int):
    """
    Retrieve a specific allocation for a book and member from the database.
    Connects to the database, executes a query to fetch the allocation with the given book ID and member ID, and returns the result as a dictionary.
    Parameters:
        book_id (int): The ID of the book.
        member_id (int): The ID of the member.
    Returns:
        dict: A dictionary representing the allocation.
    Raises:
        sqliteError: If there is an issue with the database connection or query execution.
        exception: If any other error occurs
    """
    try:
        conn = get_db_connection()
        allocation = conn.execute("SELECT * FROM Allocations WHERE book_id=? AND member_id=?;", (book_id, member_id)).fetchone()
        conn.close()
        return dict(allocation)
    except sqlite3.Error as sqliteError:
        raise Exception(f"Database error: {sqliteError}")
    except Exception as exception:
        raise Exception(f"Error: {exception}")

def add_allocation(allocation: Allocation):
    """
    Add a new allocation to the database.
    Connects to the database, executes an insert query to add the allocation's details, and commits the transaction.
    Parameters:
        allocation (Allocation): An instance of the Allocation class containing the allocation's details.
    Returns:
        None
    Raises:
        sqliteError: If there is an issue with the database connection or query execution.
        exception: If any other error occurs
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Allocations (book_id, member_id, start_date, end_date, returned, overdue) VALUES (?, ?, ?, ?, ?, ?);",
                       (allocation.book_id, allocation.member_id, allocation.start_date, allocation.end_date, allocation.returned, allocation.overdue))
        conn.commit()
        conn.close()
    except sqlite3.Error as sqliteError:
        raise Exception(f"Database error: {sqliteError}")
    except Exception as exception:
        raise Exception(f"Error: {exception}")

def edit_allocation(allocation: Allocation):
    """
    Edit an existing allocation's details in the database.
    Connects to the database, executes an update query to modify the allocation's details, and commits the transaction.
    Parameters:
        allocation (Allocation): An instance of the Allocation class containing the updated allocation's details.
    Returns:
        None
    Raises:
        sqliteError: If there is an issue with the database connection or query execution.
        exception: If any other error occurs
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE Allocations SET book_id=?, member_id=?, start_date=?, end_date=?, returned=?, overdue=? WHERE id=?;",
                       (allocation.book_id, allocation.member_id, allocation.start_date, allocation.end_date, allocation.returned, allocation.overdue, allocation.id))
        conn.commit()
        conn.close()
    except sqlite3.Error as sqliteError:
        raise Exception(f"Database error: {sqliteError}")
    except Exception as exception:
        raise Exception(f"Error: {exception}")

def delete_allocation(allocation_id: int):
    """
    Delete an allocation from the database by its ID.
    Connects to the database, executes a delete query to remove the allocation with the given ID, and commits the transaction.
    Parameters:
        allocation_id (int): The ID of the allocation to delete.
    Returns:
        None
    Raises:
        sqliteError: If there is an issue with the database connection or query execution.
        exception: If any other error occurs
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Allocations WHERE id=?;", (allocation_id,))
        conn.commit()
        conn.close()
    except sqlite3.Error as sqliteError:
        raise Exception(f"Database error: {sqliteError}")
    except Exception as exception:
        raise Exception(f"Error: {exception}")
