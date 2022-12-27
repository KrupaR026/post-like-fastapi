from fastapi import APIRouter, status, Depends
from server.user.schemas import UserBase, UserUpdate
from server.user.model import User
from datetime import datetime
from server.database import get_db
from sqlalchemy.orm import Session

userRouter = APIRouter()


@userRouter.post("/user", status_code=status.HTTP_201_CREATED)
def create_new_user(user: UserBase, db: Session = Depends(get_db)):
    """create the new user

    Args:
        user (UserBase): _description_
    """
    new_user = User(username=user.username, email=user.email)

    db.add(new_user)
    db.commit()
    return {"message": "User added successfully"}


@userRouter.get("/user", status_code=status.HTTP_200_OK)
def get_user(db: Session = Depends(get_db)):
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
def update_user(id: str, user: UserUpdate, db: Session = Depends(get_db)):
    """Put method to update the exixting user by id

    Args:
        id (str): _description_
        user (UserBase): _description_

    Returns:
        _type_: _description_
    """
    user_to_update = filter_query(id).first()

    user_to_update.updated_at = datetime.now()
    data_dict = user.dict(exclude_unset=True)

    for key, value in data_dict.items():
        setattr(user_to_update, key, value)

    db.commit()
    return {"message": "User updated successfully"}


@userRouter.delete("/user/{id}")
def delete_user(id: str, db: Session = Depends(get_db)):
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


def filter_query(id, db: Session = Depends(get_db)):

    return db.query(User).filter(User.id == id)
