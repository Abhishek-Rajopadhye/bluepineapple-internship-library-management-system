from app.database import get_db_connection
from app.models import Book
import sqlite3

def get_all_books():
    """
    Retrieve all books from the database.
    Connects to the database, executes a query to fetch all books, and returns the results as a list of dictionaries.
    Parameters:
        None
    Returns:
        list: A list of dictionaries, each representing a book.
    Raises:
        sqlite3.Error: If there is an issue with the database connection or query execution.
        Exception: If any other error occurs.
    """
    try:
        conn = get_db_connection()
        books = conn.execute("SELECT * FROM Books;").fetchall()
        conn.close()
        return [dict(book) for book in books]
    except sqlite3.Error as sqliteError:
        raise sqlite3.Error(f"Database error: {sqliteError}")
    except Exception as exception:
        raise Exception(f"Error: {exception}")

def get_book(book_id: int):
    """
    Retrieve a specific book from the database by its ID.
    Connects to the database, executes a query to fetch the book with the given ID, and returns the result as a dictionary.
    Parameters:
        book_id (int): The ID of the book to retrieve.
    Returns:
        dict: A dictionary representing the book.
    Raises:
        ValueError: If the book ID is not a positive integer.
        KeyError: If the book is not found.
        sqlite3.Error: If there is an issue with the database connection or query execution.
        Exception: If any other error occurs.
    """
    try:
        if(book_id <= 0):
            raise ValueError("Book ID must be a positive integer")

        conn = get_db_connection()
        book = conn.execute("SELECT * FROM Books WHERE id=?;", (book_id,)).fetchone()
        conn.close()
        
        if(not book):
            raise KeyError("Book not found")
        
        return dict(book)

    except sqlite3.Error as sqliteError:
        raise sqlite3.Error(f"Database error: {sqliteError}")
    except Exception as exception:
        raise Exception(f"Error: {exception}")

def get_book_by_name(book_name: str):
    """
    Retrieve a specific book from the database by its name.
    Connects to the database, executes a query to fetch the book with the given name, and returns the result as a dictionary.
    Parameters:
        book_name (str): The name of the book to retrieve.
    Returns:
        dict: A dictionary representing the book.
    Raises:
        ValueError: If the book name is empty.
        KeyError: If the book is not found.
        sqlite3.Error: If there is an issue with the database connection or query execution.
        Exception: If any other error occurs.
    """
    try:
        if(book_name == ""):
            raise ValueError("Book Name must be valid")

        conn = get_db_connection()
        book = conn.execute("SELECT * FROM Books WHERE name=?;", (book_name,)).fetchone()
        conn.close()
        
        if(not book):
            raise KeyError("Book not found")
        
        return dict(book)

    except sqlite3.Error as sqliteError:
        raise sqlite3.Error(f"Database error: {sqliteError}")
    except Exception as exception:
        raise Exception(f"Error: {exception}")

def add_book(book: Book):
    """
    Add a new book to the database.
    Connects to the database, executes an insert query to add the book's details, and commits the transaction.
    Parameters:
        book (Book): An instance of the Book class containing the book's details.
    Returns:
        None
    Raises:
        sqlite3.Error: If there is an issue with the database connection or query execution.
        sqlite3.IntegrityError: If there is a constraint violation or duplicate entry.
        Exception: If any other error occurs.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Books (name, author, total_copies) VALUES (?, ?, ?);", (book.name, book.author, book.total_copies))
        conn.commit()
        conn.close()
    except sqlite3.Error as sqliteError:
        raise sqlite3.Error(f"Database error: {sqliteError}")
    except sqlite3.IntegrityError:
        raise Exception("Integrity error: Possible duplicate or constraint violation")
    except Exception as exception:
        raise Exception(f"Error: {exception}")

def edit_book(book_id:int, book: Book):
    """
    Edit an existing book's details in the database.
    Connects to the database, executes an update query to modify the book's details, and commits the transaction.
    Parameters:
        book_id (int): The ID of the book to update/edit.
        book (Book): An instance of the Book class containing the updated book's details.
    Returns:
        None
    Raises:
        ValueError: If the book ID is not a positive integer.
        KeyError: If the book is not found.
        sqlite3.Error: If there is an issue with the database connection or query execution.
        Exception: If any other error occurs.
    """
    try:
        if(book_id <= 0):
            raise ValueError("Book ID must be a positive integer")

        conn = get_db_connection()
        cursor = conn.cursor()
        book = conn.execute("SELECT * FROM Books WHERE id=?;", (book_id,)).fetchone()
        
        if(not book):
            raise KeyError("Book not found")
        
        cursor.execute("UPDATE Books SET name=?, author=?, total_copies=?, allocated_copies=? WHERE id=?;", (book.name, book.author, book.total_copies, book.allocated_copies, book_id))
        conn.commit()
        conn.close()
    except sqlite3.Error as sqliteError:
        raise sqlite3.Error(f"Database error: {sqliteError}")
    except Exception as exception:
        raise RuntimeError(f"Error: {exception}")

def delete_book(book_id: int):
    """
    Delete a book from the database by its ID.
    Connects to the database, executes a delete query to remove the book with the given ID, and commits the transaction.
    Parameters:
        book_id (int): The ID of the book to delete.
    Returns:
        None
    Raises:
        ValueError: If the book ID is not a positive integer.
        KeyError: If the book is not found.
        sqlite3.Error: If there is an issue with the database connection or query execution.
        Exception: If any other error occurs.
    """
    try:
        if(book_id <= 0):
            raise ValueError("Book ID must be a positive integer")

        conn = get_db_connection()
        cursor = conn.cursor()
        book = conn.execute("SELECT * FROM Books WHERE id=?;", (book_id,)).fetchone()
        
        if(not book):
            raise KeyError("Book not found")

        cursor.execute("DELETE FROM Books WHERE id=?;", (book_id,))
        conn.commit()
        conn.close()
    except sqlite3.Error as sqliteError:
        raise sqlite3.Error(f"Database error: {sqliteError}")
    except Exception as exception:
        raise Exception(f"Error: {exception}")
