from pydantic import BaseModel
from typing import Optional


class PostBase(BaseModel):
    """Create the schema for the Post table

    Args:
        BaseModel (_type_): _description_
    """

    title: str
    description: str
    user_id: str

    class Config:
        orm_mode = True


class PostUpdate(BaseModel):
    title: Optional[str] = None
    dexcription: Optional[str] = None
    user_id: Optional[str] = None
