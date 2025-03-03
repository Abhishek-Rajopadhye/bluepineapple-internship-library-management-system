from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.models import Member
import app.data_logic.members_data_logic as member_crud
import sqlite3

router = APIRouter(tags=["Members"])

@router.get("/")
def getMembers() -> list:
    """
    Retrieve all members from the database.
    Calls the get_all_members function from the member_crud module to fetch all members and returns the result.
    Parameters:
        None
    Returns:
        members (list): A list of dictionaries, each representing a member.
    Raises:
        HTTPException (500): If any error occurs during fetching of members.
    """
    try:
        members = member_crud.get_all_members()
        return JSONResponse(content=members, status_code=200)
    except sqlite3.Error as databaseError:
        raise HTTPException(status_code=500, detail=f"Database error: {databaseError}")
    except Exception as exception:
        raise HTTPException(status_code=500, detail=f"Error: {exception}")

@router.get("/{member_id}")
def getMember(member_id: int) -> dict:
    """
    Retrieve a specific member from the database by their ID.
    Calls the get_member function from the member_crud module to fetch the member with the given ID and returns the result.
    Parameters:
        member_id (str): The ID of the member to retrieve.
    Returns:
        member (dict): A dictionary representing the member.
    Raises:
        HTTPException (400): If the member ID is not a positive integer.
        HTTPException (404): If the member is not found.
        HTTPException (500): If any error occurs during fetching of the member.
    """
    try:
        member = member_crud.get_member(member_id)
        return JSONResponse(content=member, status_code=200)
    except ValueError as valueError:
        raise HTTPException(status_code=400, detail=str(valueError))
    except KeyError as memberNotFound:
        raise HTTPException(status_code=404, detail=str(memberNotFound))
    except sqlite3.Error as databaseError:
        raise HTTPException(status_code=500, detail=f"Database error: {databaseError}")
    except Exception as exception:
        raise HTTPException(status_code=500, detail=f"Error: {exception}")

@router.get("/name={member_name}")
def getMemberByName(member_name: str) -> dict:
    """
    Retrieve a specific member from the database by their name.
    Calls the get_member_by_name function from the member_crud module to fetch the member with the given name and returns the result.
    Parameters:
        member_name (str): The name of the member to retrieve.
    Returns:
        member (dict): A dictionary representing the member.
    Raises:
        HTTPException (404): If the member is not found.
        HTTPException (500): If any error occurs during fetching of the member.
    """
    try:
        member = member_crud.get_member_by_name(member_name)
        return JSONResponse(content=member, status_code=200)
    except KeyError as memberNotFound:
        raise HTTPException(status_code=404, detail=str(memberNotFound))
    except sqlite3.Error as databaseError:
        raise HTTPException(status_code=500, detail=f"Database error: {databaseError}")
    except Exception as exception:
        raise HTTPException(status_code=500, detail=f"Error: {exception}")

@router.post("/")
def addMember(member: Member) -> dict:
    """
    Add a new member to the database.
    Calls the add_member function from the member_crud module to add the member's details to the database.
    Parameters:
        member (Member): An instance of the Member class containing the member's details.
    Returns:
        msg (dict): A success message.
    Raises:
        HTTPException (400): If there is an integrity error.
        HTTPException (500): If any error occurs during adding of the member.
    """
    try:
        member_crud.add_member(member)
        return JSONResponse(content={"msg": "Success"}, status_code=200)
    except sqlite3.IntegrityError as duplicateError:
        raise HTTPException(status_code=400, detail=f"Integrity error: {duplicateError}")
    except sqlite3.Error as databaseError:
        raise HTTPException(status_code=500, detail=f"Database error: {databaseError}")
    except Exception as exception:
        raise HTTPException(status_code=500, detail=f"Error: {exception}")

@router.put("/{member_id}")
def editMember(member_id: str, member: Member) -> dict:
    """
    Edit an existing member's details in the database.
    Calls the edit_member function from the member_crud module to modify the member's details in the database.
    Parameters:
        member_id (str): The ID of the member to edit.
        member (Member): An instance of the Member class containing the updated member's details.
    Returns:
        msg (dict): A success message.
    Raises:
        HTTPException (400): If the member ID is not a positive integer.
        HTTPException (404): If the member is not found.
        HTTPException (500): If any error occurs during editing of the member.
    """
    try:
        member_crud.edit_member(int(member_id), member)
        return JSONResponse(content={"msg": "Success"}, status_code=200)
    except ValueError as valueError:
        raise HTTPException(status_code=400, detail=str(valueError))
    except KeyError as memberNotFound:
        raise HTTPException(status_code=404, detail=str(memberNotFound))
    except sqlite3.Error as databaseError:
        raise HTTPException(status_code=500, detail=f"Database error: {databaseError}")
    except Exception as exception:
        raise HTTPException(status_code=500, detail=f"Error: {exception}")

@router.delete("/{member_id}")
def deleteMember(member_id: str) -> dict:
    """
    Delete a member from the database by their ID.
    Calls the delete_member function from the member_crud module to remove the member with the given ID from the database.
    Parameters:
        member_id (str): The ID of the member to delete.
    Returns:
        msg (dict): A success message.
    Raises:
        HTTPException (400): If the member ID is not a positive integer.
        HTTPException (404): If the member is not found.
        HTTPException (500): If any error occurs during deleting of the member.
    """
    try:
        member_crud.delete_member(int(member_id))
        return JSONResponse(content={"msg": "Success"}, status_code=200)
    except ValueError as valueError:
        raise HTTPException(status_code=400, detail=str(valueError))
    except KeyError as memberNotFound:
        raise HTTPException(status_code=404, detail=str(memberNotFound))
    except sqlite3.Error as databaseError:
        raise HTTPException(status_code=500, detail=f"Database error: {databaseError}")
    except Exception as exception:
        raise HTTPException(status_code=500, detail=f"Error: {exception}")