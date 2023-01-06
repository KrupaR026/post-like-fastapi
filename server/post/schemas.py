from pydantic import BaseModel
from typing import Optional


class PostBase(BaseModel):
    """Create the schema for the Post table"""

    title: str
    description: str
    post_type: str
    post_display_user: str

    class Config:
        orm_mode = True


class PostUpdate(BaseModel):
    """Create the schema for update the post"""

    title: Optional[str] = None
    description: Optional[str] = None
    post_type: Optional[str] = None
    post_display_user: Optional[str] = None
