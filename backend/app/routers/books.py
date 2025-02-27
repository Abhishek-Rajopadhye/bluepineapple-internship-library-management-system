from fastapi import APIRouter, HTTPException
from models import Book
import data_logic.books_data_logic as book_crud

router = APIRouter(tags=["Books"])

@router.get("/")
def getBooks() -> list:
    """
    Summary:
        Retrieve all books from the database.
    Working:
        Calls the get_all_books function from the book_crud module to fetch all books and returns the result.
    Parameters:
        None
    Returns:
        list: A list of dictionaries, each representing a book.
    Raises:
        HTTPException (500): If there is an issue with fetching the books.
    """
    try:
        books = book_crud.get_all_books()
        return books, 200
    except KeyError as keyError:
        raise HTTPException(status_code=400, detail=str(keyError))
    except RuntimeError as runtimeError:
        raise HTTPException(status_code=500, detail=str(runtimeError))

@router.get("/{book_id}")
def getBook(book_id: str) -> dict:
    """
    Retrieve a specific book from the database by its ID.
    Calls the get_book function from the book_crud module to fetch the book with the given ID and returns the result.
    Parameters:
        book_id (str): The ID of the book to retrieve.
    Returns:
        dict: A dictionary representing the book.
    Raises:
        HTTPException (500): If there is an issue with fetching the book.
    """
    try:
        book = book_crud.get_book(int(book_id))
        return book, 200
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/")
def addBook(book: Book) -> dict:
    """
    Add a new book to the database.
    Calls the add_book function from the book_crud module to add the book's details to the database.
    Parameters:
        book (Book): An instance of the Book class containing the book's details.
    Returns:
        dict: A success message.
    Raises:
        HTTPException (500): If there is an issue with adding the book.
    """
    try:
        book_crud.add_book(book)
        return {"msg": "Success"}, 200
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{book_id}")
def editBook(book_id: str, book: Book) -> dict:
    """
    Edit an existing book's details in the database.
    Calls the edit_book function from the book_crud module to modify the book's details in the database.
    Parameters:
        book_id (str): The ID of the book to edit.
        book (Book): An instance of the Book class containing the updated book's details.
    Returns:
        dict: A success message.
    Raises:
        HTTPException (500): If there is an issue with editing the book.
    """
    try:
        book_crud.edit_book(int(book_id), book)
        return {"msg": "Success"}, 200
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{book_id}")
def deleteBook(book_id: str) -> dict:
    """
    Delete a book from the database by its ID.
    Calls the delete_book function from the book_crud module to remove the book with the given ID from the database.
    Parameters:
        book_id (str): The ID of the book to delete.
    Returns:
        dict: A success message.
    Raises:
        HTTPException (500): If there is an issue with deleting the book.
    """
    try:
        book_crud.delete_book(int(book_id))
        return {"msg": "Success"}, 200
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
