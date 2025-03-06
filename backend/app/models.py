from pydantic import BaseModel
from datetime import date
from typing import Optional

class BookBase(BaseModel):
    """
    Base model for a book.
    Attributes:
        name (str): The name of the book.
        author (str): The author of the book.
        total_copies (int): The total number of copies of the book.
        allocated_copies (int): The number of allocated copies of the book.
    """
    name: str
    author: str
    total_copies: int
    allocated_copies: int

class Book(BookBase):
    """
    Model for a book with an ID.
    Attributes:
        id (int): The ID of the book.
    """
    id: int

class MemberBase(BaseModel):
    """
    Base model for a member.
    Attributes:
        name (str): The name of the member.
        email (Optional[str]): The email of the member.
        phone (Optional[str]): The phone number of the member.
    """
    name: str
    email: Optional[str]
    phone: Optional[str]

class Member(MemberBase):
    """
    Model for a member with an ID.
    Attributes:
        id (int): The ID of the member.
    """
    id: int

class AllocationBase(BaseModel):
    """
    Base model for an allocation.
    Attributes:
        book_id (int): The ID of the allocated book.
        member_id (int): The ID of the member to whom the book is allocated.
        start_date (date): The start date of the allocation.
        end_date (date): The end date of the allocation.
    """
    book_id: int
    member_id: int
    start_date: date
    end_date: date

class Allocation(AllocationBase):
    """
    Model for an allocation with an ID, returned status, and overdue status.
    Attributes:
        id (int): The ID of the allocation.
        returned (bool): Indicates whether the book has been returned.
        overdue (bool): Indicates whether the allocation is overdue.
    """
    id: int
    returned: bool = False
    overdue: bool = False
