from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.models import Book
import app.data_logic.books_data_logic as book_crud
import sqlite3

router = APIRouter(tags=["Books"])

@router.get("/")
def getBooks() -> list:
    """
    Retrieve all books from the database.
    Calls the get_all_books function from the book_crud module to fetch all books and returns the result.
    Parameters:
        None
    Returns:
        books (list): A list of dictionaries, each representing a book.
    Raises:
        HTTPException (500): If any error occurs during fetching of books.
    """
    try:
        books = book_crud.get_all_books()
        return JSONResponse(content=books, status_code=200)
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")

@router.get("/{book_id}")
def getBook(book_id: str) -> dict:
    """
    Retrieve a specific book from the database by its ID.
    Calls the get_book function from the book_crud module to fetch the book with the given ID and returns the result.
    Parameters:
        book_id (str): The ID of the book to retrieve.
    Returns:
        book (dict): A dictionary representing the book.
    Raises:
        HTTPException (400): If the book ID is not a positive integer.
        HTTPException (404): If the book is not found.
        HTTPException (500): If any error occurs during fetching of the book.
    """
    try:
        book = book_crud.get_book(int(book_id))
        return JSONResponse(content=book, status_code=200)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")

@router.post("/")
def addBook(book: Book) -> dict:
    """
    Add a new book to the database.
    Calls the add_book function from the book_crud module to add the book's details to the database.
    Parameters:
        book (Book): An instance of the Book class containing the book's details.
    Returns:
        msg (dict): A success message.
    Raises:
        HTTPException (400): If there is an integrity error.
        HTTPException (500): If any error occurs during adding of the book.
    """
    try:
        book_crud.add_book(book)
        return JSONResponse(content={"msg": "Success"}, status_code=200)
    except sqlite3.IntegrityError as e:
        raise HTTPException(status_code=400, detail=f"Integrity error: {e}")
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")

@router.put("/{book_id}")
def editBook(book_id: str, book: Book) -> dict:
    """
    Edit an existing book's details in the database.
    Calls the edit_book function from the book_crud module to modify the book's details in the database.
    Parameters:
        book_id (str): The ID of the book to edit.
        book (Book): An instance of the Book class containing the updated book's details.
    Returns:
        msg (dict): A success message.
    Raises:
        HTTPException (400): If the book ID is not a positive integer.
        HTTPException (404): If the book is not found.
        HTTPException (500): If any error occurs during editing of the book.
    """
    try:
        book_crud.edit_book(int(book_id), book)
        return JSONResponse(content={"msg": "Success"}, status_code=200)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")

@router.delete("/{book_id}")
def deleteBook(book_id: str) -> dict:
    """
    Delete a book from the database by its ID.
    Calls the delete_book function from the book_crud module to remove the book with the given ID from the database.
    Parameters:
        book_id (str): The ID of the book to delete.
    Returns:
        msg (dict): A success message.
    Raises:
        HTTPException (400): If the book ID is not a positive integer.
        HTTPException (404): If the book is not found.
        HTTPException (500): If any error occurs during deleting of the book.
    """
    try:
        book_crud.delete_book(int(book_id))
        return JSONResponse(content={"msg": "Success"}, status_code=200)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")
