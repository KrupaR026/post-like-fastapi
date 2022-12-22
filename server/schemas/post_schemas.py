from pydantic import BaseModel
from typing import Optional


class PostBase(BaseModel):
    """Create the schema for the Post table

    Args:
        BaseModel (_type_): _description_
    """    
    title: Optional[str]
    description: Optional[str]
    user_id: Optional[str]

    class Config:
        orm_mode = True