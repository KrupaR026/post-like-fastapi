from fastapi import APIRouter, status
from server.schemas.user_schemas import UserBase
from server.models.user_model import User
from server.database.database import SessionLocal
from datetime import datetime

userRouter = APIRouter()
db = SessionLocal()

@userRouter.post("/user", status_code=status.HTTP_201_CREATED)
def create_new_user(user: UserBase):
    """create the new user

    Args:
        user (UserBase): _description_
    """    
    new_user = User(
        username = user.username,
        email = user.email
    )

    db.add(new_user)
    db.commit()
    return {"message": "User added successfully"}


@userRouter.get("/user", status_code=status.HTTP_200_OK)
def get_user():
    """Get method to get the existing all the user

    Returns:
        _type_: _description_
    """    
    users = db.query(User).all()
    return users   


@userRouter.get("/user/{id}", status_code=status.HTTP_200_OK)
def get_user_by_id(id: str):
    """Get method to get the particular user by id

    Args:
        id (str): _description_

    Returns:
        _type_: _description_
    """    
    user = filter_query(id).first()
    return user


@userRouter.put("/user/{id}", status_code=status.HTTP_200_OK)
def update_user(id: str, user: UserBase):
    """Put method to update the exixting user by id

    Args:
        id (str): _description_
        user (UserBase): _description_

    Returns:
        _type_: _description_
    """    
    user_to_update = filter_query(id).first()
    user_to_update.updated_at = datetime.now()
    user_to_update.username = (user.username,)
    user_to_update.email = (user.email,)

    db.commit()
    return {"message": "User updated successfully"}


@userRouter.delete("/user/{id}")
def delete_user(id: str):
    """Delete method to delete a user by id

    Args:
        id (str): _description_

    Returns:
        _type_: _description_
    """    
    user_to_delete = filter_query(id).first()
    db.delete(user_to_delete)
    db.commit()

    return {"data": user_to_delete, "message": "User delete successfully"}


def filter_query(id):

    return db.query(User).filter(User.id == id)
