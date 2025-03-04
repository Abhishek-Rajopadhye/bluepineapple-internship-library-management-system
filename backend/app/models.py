from pydantic import BaseModel
from datetime import date
from typing import Optional

class BookBase(BaseModel):
    name: str
    author: str
    total_copies: int
    allocated_copies: int

class Book(BookBase):
    id: int

class MemberBase(BaseModel):
    name: str
    email: Optional[str]
    phone: Optional[str]

class Member(MemberBase):
    id: int

class AllocationBase(BaseModel):
    book_id: int
    member_id: int
    start_date: date
    end_date: date

class Allocation(AllocationBase):
    id: int
    returned: bool = False
    overdue: bool = False
