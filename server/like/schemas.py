from pydantic import BaseModel


class LikeBase(BaseModel):
    """Create the schema for the Like table

    Args:
        BaseModel (_type_): _description_
    """    
    post_id: str
    user_id: str
    username: str

    class Config:
        orm_mode = True


