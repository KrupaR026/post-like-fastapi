from fastapi import APIRouter, status, Depends
from server.user.schemas import UserBase, UserUpdate
from server.user.model import User
from sqlalchemy.orm import Session
from server.database import get_db

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

    user_id = db.query(User.id).order_by(User.created_at.desc()).first()
    return {user_id, "message: User added successfully"}


@userRouter.get("/user", status_code=status.HTTP_200_OK)
def get_user(db: Session = Depends(get_db)):
    """Get method to get the existing all the user

    Returns:
        _type_: _description_
    """
    all_users = db.query(User).all()
    active_user = [i for i in all_users if i.is_delete == False]
    return active_user


@userRouter.get("/user/{id}", status_code=status.HTTP_200_OK)
def get_user_by_id(id: str, db: Session = Depends(get_db)):
    """Get method to get the particular user by id

    Args:
        id (str): _description_

    Returns:
        _type_: _description_
    """
    user = filter_query(db, id).first()
    if user is not None:
        if user.is_delete == False:
            return user
        else:
            return "This user has been deleted earlier so the data cannot be retrieved."
    else:
        return "This ID cannot be exists."


@userRouter.put("/user/{id}", status_code=status.HTTP_200_OK)
def update_user(id: str, user: UserUpdate, db: Session = Depends(get_db)):
    """Put method to update the exixting user by id

    Args:
        id (str): _description_
        user (UserBase): _description_

    Returns:
        _type_: _description_
    """
    user_to_update = filter_query(db, id).first()
    if user_to_update is not None:
        if user_to_update.is_delete == False:
            data_dict = user.dict(exclude_unset=True)

            for key, value in data_dict.items():
                setattr(user_to_update, key, value)

            db.commit()
            return {"message": "User updated successfully"}

        else:
            return "This user has been deleted earlier so the data cannot be update."

    else:
        return "This ID cannot be exists."


@userRouter.delete("/user/{id}")
def delete_user(id: str, db: Session = Depends(get_db)):
    """Delete method to delete a user by id

    Args:
        id (str): _description_

    Returns:
        _type_: _description_
    """
    user_to_delete = filter_query(db, id).first()
    if user_to_delete is not None:
        filter_query(db, id).update({"is_delete": True})
        db.commit()
        return {"message": "User delete successfully"}
    else:
        return "This ID does not exists."


def filter_query(db, id):
    return db.query(User).filter(User.id == id)
