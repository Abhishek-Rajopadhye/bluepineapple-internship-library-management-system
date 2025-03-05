from app.database import get_db_connection
import sqlite3

def get_history():
    """
    Retrieve all historic allocations from the database.
    Connects to the database, executes a query to fetch all historic allocations, and returns the results as a list of dictionaries.
    Parameters:
        None
    Returns:
        history (list): A list of dictionaries, each representing a historic allocation.
    Raises:
        sqliteError: If there is an issue with the database connection or query execution.
        exception: If any other error occurs
    """
    try:
        conn = get_db_connection()
        history = conn.execute("SELECT * FROM History;").fetchall()
        conn.close()
        return [dict(allocation) for allocation in history]
    except sqlite3.Error as sqliteError:
        raise sqlite3.Error(f"Database error: {sqliteError}")
    except Exception as exception:
        raise Exception(f"Error: {exception}")
