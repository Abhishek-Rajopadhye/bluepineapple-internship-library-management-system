
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
import app.data_logic.history_data_logic as history_crud
import sqlite3

router = APIRouter(tags=["History"])

@router.get("/")
def getAllocations() -> list:
    """
    Retrieve all allocations history from the database.
    Calls the get_history function from the history_crud module to fetch all historic allocations and returns the result.
    Parameters:
        None
    Returns:
        history (list): A list of dictionaries, each representing a historic allocation.
    Raises:
        HTTPException (500): If any error occurs during fetching of historic allocations.
    """
    try:
        history = history_crud.get_history()
        return JSONResponse(content=history, status_code=200)
    except sqlite3.Error as databaseError:
        raise HTTPException(status_code=500, detail=f"Database error: {databaseError}")
    except Exception as exception:
        raise HTTPException(status_code=500, detail=f"Error: {exception}")