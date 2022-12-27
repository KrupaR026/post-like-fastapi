from fastapi import APIRouter, status, Depends
from server.post.schemas import PostBase, PostUpdate
from server.post.model import Post
from datetime import datetime
from server.database import get_db
from sqlalchemy.orm import Session

postRouter = APIRouter()

@postRouter.post("/post/{public_or_private}", status_code=status.HTTP_201_CREATED)
def create_new_post(public_or_private: str, post: PostBase, db: Session = Depends(get_db)):
    """create the new post

    Args:
        post (PostBase): _description_

    Returns:
        _type_: _description_
    """      
    new_post = Post(
        title = post.title,
        description = post.description,
        user_id = post.user_id,
        post_type = public_or_private
    )
    db.add(new_post)
    db.commit()
    return {"message": "Post added successfully"}


@postRouter.put("/post/{id}", status_code=status.HTTP_200_OK)
def update_post(id: str, post: PostUpdate, db: Session = Depends(get_db)):
    """Edit the post by post id

    Args:
        id (str): _description_
        post (PostBase): _description_

    Returns:
        _type_: _description_
    """ 
    post_to_update = filter_query(id)

    post_to_update.updated_at = datetime.now()
    post_dict = post.dict(exclude_unset=True)

    for key, value in post_dict.items():
        setattr(post_to_update, key, value)

    db.commit()
    return {"message": "Post updated successfully"}


@postRouter.get("/post", status_code=status.HTTP_404_NOT_FOUND)
def get_all_the_post_with_like_count(db: Session = Depends(get_db)):
    """get all the post with total likes and post details

    Returns:
        _type_: _description_
    """    
    post = db.query(Post).all()
    return post



@postRouter.get("/post/{post_id}")
def post_and_total_like(post_id: str, db: Session = Depends(get_db)):
    """get the post and total likes by specific post id

    Args:
        post_id (str): _description_

    Returns:
        _type_: _description_
    """    
    post = db.query(Post).filter(Post.id == post_id).first()
    return post


@postRouter.delete("/post/{id}")
def delete_post(id: str, db: Session = Depends(get_db)):
    """Delete method to delete a post by id

    Args:
        id (str): _description_

    Returns:
        _type_: _description_
    """    
    post_to_delete = filter_query(id)
    db.delete(post_to_delete)
    db.commit()

    return {"data": post_to_delete, "message": "Post delete successfully"}


def filter_query(id, db: Session = Depends(get_db)):

    return db.query(Post).filter(Post.id == id).first()

