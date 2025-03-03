import sqlite3
import pathlib

DB_PATH = pathlib.Path("data/library.sql")

def get_db_connection():
    """
    Establish a connection to the database.
    Connects to the SQLite database specified by DB_PATH and sets the row factory to sqlite3.Row for dictionary-like access to rows.
    If the database file does not exist, it creates the file.
    Parameters:
        None
    Returns:
        conn (sqlite3.Connection): A connection object to the SQLite database.
    Raises:
        sqlite3.Error: If there is an issue with the database connection or query execution.
        Exception: If any other error occurs
    """
    try:
        # Check if the database file exists, if not, create it
        if not DB_PATH.exists():
            DB_PATH.parent.mkdir(parents=True, exist_ok=True)
            DB_PATH.touch()

        conn = sqlite3.connect(str(DB_PATH.absolute()))
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as sqliteError:
        raise Exception(f"Database connection error: {sqliteError}")
    except Exception as exception:
        raise Exception(f"Error: {exception}")

def init_db():
    """
    Initialize the database with the required tables.
    Connects to the database, creates the Books, Members, and Allocations tables if they do not exist, and commits the changes.
    Parameters:
        None
    Returns:
        None
    Raises:
        sqlite3.Error: If there is an issue with the database connection or query execution.
        Exception: If any other error occurs
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            author TEXT NOT NULL,
            total_copies INTEGER NOT NULL,
            allocated_copies INTEGER DEFAULT 0
        );
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE,
            phone TEXT
        );
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Allocations (
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
        conn.close()
    except sqlite3.Error as sqliteError:
        raise Exception(f"Database initialization error: {sqliteError}")
    except Exception as exception:
        raise Exception(f"Error: {exception}")

init_db()
