from pydantic import BaseModel


class LikeBase(BaseModel):
    """Create the schema for the Like table"""

    post_id: str
    like_by: str

    class Config:
        orm_mode = True
