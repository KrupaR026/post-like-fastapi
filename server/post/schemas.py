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
    post_type: str
    post_display_user: str

    class Config:
        orm_mode = True


class PostUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    post_display_user: Optional[str] = None
