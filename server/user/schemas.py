from pydantic import BaseModel
from typing import Optional


class UserBase(BaseModel):
    """Create the schema for the User table"""

    username: str
    email: str

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    """Create the schema for update the user"""

    username: Optional[str] = None
    email: Optional[str] = None
