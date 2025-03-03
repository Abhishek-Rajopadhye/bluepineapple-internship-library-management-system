from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.models import Allocation
import app.data_logic.allocations_data_logic as allocation_crud
import sqlite3

router = APIRouter(tags=["Allocations"])

@router.get("/")
def getAllocations() -> list:
    """
    Retrieve all allocations from the database.
    Calls the get_all_allocation function from the allocation_crud module to fetch all allocations and returns the result.
    Parameters:
        None
    Returns:
        allocations (list): A list of dictionaries, each representing an allocation.
    Raises:
        HTTPException (500): If any error occurs during fetching of allocations.
    """
    try:
        allocations = allocation_crud.get_all_allocation()
        return JSONResponse(content=allocations, status_code=200)
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")

@router.get("/{allocation_id}")
def getAllocation(allocation_id: str) -> dict:
    """
    Retrieve a specific allocation from the database by its ID.
    Calls the get_allocation function from the allocation_crud module to fetch the allocation with the given ID and returns the result.
    Parameters:
        allocation_id (str): The ID of the allocation to retrieve.
    Returns:
        allocation (dict): A dictionary representing the allocation.
    Raises:
        HTTPException (400): If the allocation ID is not a positive integer.
        HTTPException (404): If the allocation is not found.
        HTTPException (500): If any error occurs during fetching of the allocation.
    """
    try:
        allocation = allocation_crud.get_allocation(int(allocation_id))
        return JSONResponse(content=allocation, status_code=200)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")

@router.get("/book={book_id}")
def getAllocationsOfBook(book_id: str) -> list:
    """
    Retrieve all allocations for a specific book from the database.
    Calls the get_allocations_of_book function from the allocation_crud module to fetch all allocations for the given book ID and returns the result.
    Parameters:
        book_id (str): The ID of the book to retrieve allocations for.
    Returns:
        allocations (list): A list of dictionaries, each representing an allocation.
    Raises:
        HTTPException (400): If the book ID is not a positive integer.
        HTTPException (500): If any error occurs during fetching of allocations.
    """
    try:
        allocations = allocation_crud.get_allocations_of_book(int(book_id))
        return JSONResponse(content=allocations, status_code=200)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")

@router.get("/member={member_id}")
def getAllocationsOfMember(member_id: str) -> list:
    """
    Retrieve all allocations for a specific member from the database.
    Calls the get_allocations_of_member function from the allocation_crud module to fetch all allocations for the given member ID and returns the result.
    Parameters:
        member_id (str): The ID of the member to retrieve allocations for.
    Returns:
        allocations (list): A list of dictionaries, each representing an allocation.
    Raises:
        HTTPException (400): If the member ID is not a positive integer.
        HTTPException (404): If the member is not found.
        HTTPException (500): If any error occurs during fetching of allocations.
    """
    try:
        allocations = allocation_crud.get_allocations_of_member(int(member_id))
        return JSONResponse(content=allocations, status_code=200)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")

@router.get("/book={book_id}&member={member_id}")
def getAllocationByBookAndMember(book_id: str, member_id: str) -> dict:
    """
    Retrieve a specific allocation for a book and member from the database.
    Calls the get_allocation_by_book_and_member function from the allocation_crud module to fetch the allocation with the given book ID and member ID and returns the result.
    Parameters:
        book_id (str): The ID of the book.
        member_id (str): The ID of the member.
    Returns:
        allocation (dict): A dictionary representing the allocation.
    Raises:
        HTTPException (400): If the book ID or member ID is not a positive integer.
        HTTPException (404): If the allocation is not found.
        HTTPException (500): If any error occurs during fetching of the allocation.
    """
    try:
        allocation = allocation_crud.get_allocation_by_book_and_member(int(book_id), int(member_id))
        return JSONResponse(content=allocation, status_code=200)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")

@router.post("/")
def addAllocation(allocation: Allocation) -> dict:
    """
    Add a new allocation to the database.
    Calls the add_allocation function from the allocation_crud module to add the allocation's details to the database.
    Parameters:
        allocation (Allocation): An instance of the Allocation class containing the allocation's details.
    Returns:
        msg (dict): A success message.
    Raises:
        HTTPException (400): If there is an integrity error.
        HTTPException (500): If any error occurs during adding of the allocation.
    """
    try:
        allocation_crud.add_allocation(allocation)
        return JSONResponse(content={"msg": "Success"}, status_code=200)
    except sqlite3.IntegrityError as e:
        raise HTTPException(status_code=400, detail=f"Integrity error: {e}")
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")

@router.put("/{allocation_id}")
def editAllocation(allocation_id: str, allocation: Allocation) -> dict:
    """
    Edit an existing allocation's details in the database.
    Calls the edit_allocation function from the allocation_crud module to modify the allocation's details in the database.
    Parameters:
        allocation_id (str): The ID of the allocation to edit.
        allocation (Allocation): An instance of the Allocation class containing the updated allocation's details.
    Returns:
        msg (dict): A success message.
    Raises:
        HTTPException (400): If the allocation ID is not a positive integer.
        HTTPException (404): If the allocation is not found.
        HTTPException (500): If any error occurs during editing of the allocation.
    """
    try:
        allocation_crud.edit_allocation(int(allocation_id), allocation)
        return JSONResponse(content={"msg": "Success"}, status_code=200)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")

@router.delete("/{allocation_id}")
def deleteAllocation(allocation_id: str) -> dict:
    """
    Delete an allocation from the database by its ID.
    Calls the delete_allocation function from the allocation_crud module to remove the allocation with the given ID from the database.
    Parameters:
        allocation_id (str): The ID of the allocation to delete.
    Returns:
        msg (dict): A success message.
    Raises:
        HTTPException (400): If the allocation ID is not a positive integer.
        HTTPException (404): If the allocation is not found.
        HTTPException (500): If any error occurs during deleting of the allocation.
    """
    try:
        allocation_crud.delete_allocation(int(allocation_id))
        return JSONResponse(content={"msg": "Success"}, status_code=200)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")