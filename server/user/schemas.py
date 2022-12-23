from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    """Create the schema for the User table

    Args:
        BaseModel (_type_): _description_
    """    
    username: str
    email: str

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None