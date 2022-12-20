from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    description: str
    user_id: str

    class Config:
        orm_mode = True