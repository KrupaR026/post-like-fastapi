from pydantic import BaseModel


class LikeBase(BaseModel):
    post_id: str
    user_id: str
    userrname: str

    class Config:
        orm_mode = True


class LikeDetails(LikeBase):
    userrname: str
    time: str

    class Config:
        orm_mode = True