from pydantic import BaseModel

class UserBase(BaseModel):
    """Create the schema for the User table

    Args:
        BaseModel (_type_): _description_
    """    
    username: str
    email: str

    class Config:
        orm_mode = True