from fastapi import APIRouter, status, Depends
from server.post.schemas import PostBase, PostUpdate
from server.post.model import Post
from server.like.model import Like
from datetime import datetime
from server.database import get_db
from sqlalchemy.orm import Session

postRouter = APIRouter()


@postRouter.post("/post", status_code=status.HTTP_201_CREATED)
def create_new_post(post: PostBase, db: Session = Depends(get_db)):
    """create the new post

    Args:
        post (PostBase): _description_

    Returns:
        _type_: _description_
    """
    new_post = Post(
        title=post.title,
        description=post.description,
        user_id=post.user_id,
        post_type=post.post_type,
        post_display_user=post.post_display_user,
    )
    db.add(new_post)
    db.commit()
    return {"message": "Post added successfully"}


@postRouter.put("/post/{post_id}/{user_id}", status_code=status.HTTP_200_OK)
def update_post(
    post_id: str, user_id: str, post: PostUpdate, db: Session = Depends(get_db)
):
    """Edit the post by post id

    Args:
        id (str): _description_
        post (PostBase): _description_

    Returns:
        _type_: _description_
    """
    post_to_update = filter_query(db, post_id)
    post_user_id_column = db.query(Post.user_id).filter(Post.id == post_id).first()
    post_user_id = post_user_id_column["user_id"]
    if post_user_id == user_id:

        post_to_update.updated_at = datetime.now()
        post_dict = post.dict(exclude_unset=True)

        for key, value in post_dict.items():
            setattr(post_to_update, key, value)

        db.commit()
        return {"message": "Post updated successfully"}
    return "You have no rights to update the post"


@postRouter.get("/post", status_code=status.HTTP_404_NOT_FOUND)
def get_all_the_post_with_like_count(db: Session = Depends(get_db)):
    """get all the post with total likes and post details

    Returns:
        _type_: _description_
    """
    # all_post = db.query(Post).all()
    all_post = db.query(Post).filter(Post.post_type == "public").all()
    # public_post = all_post
    return all_post


@postRouter.get("/post/{post_id}/{user_id}")
def post_and_total_like(post_id: str, user_id: str, db: Session = Depends(get_db)):
    """get the post and total likes by specific post id

    Args:
        post_id (str): _description_

    Returns:
        _type_: _description_
    """
    post = filter_query(db, post_id)
    # return post

    two_post_column = (
        db.query(Post.post_type, Post.post_display_user)
        .filter(Post.id == post_id)
        .first()
    )
    public_or_private = two_post_column["post_type"]
    post_user_id_filed = db.query(Post.user_id).filter(Post.id == post_id).first()
    post_user_id = post_user_id_filed["user_id"]

    if public_or_private == "public":
        return post

    elif public_or_private == "private":
        if user_id == post_user_id:
            return post
        else:
            return "Sorry, This post is private. So you can't see it."

    else:
        display_all_users = two_post_column["post_display_user"]
        display_user_list = display_all_users.split()
        if user_id in display_user_list or user_id == post_user_id:
            return post
        else:
            return "Sorry, This post is private. So you can't see it."


@postRouter.delete("/post/{post_id}/{user_id}")
def delete_post(post_id: str, user_id: str, db: Session = Depends(get_db)):
    """Delete method to delete a post by id

    Args:
        id (str): _description_

    Returns:
        _type_: _description_
    """
    post_to_delete = filter_query(db, post_id)
    post_user_id_column = db.query(Post.user_id).filter(Post.id == post_id).first()
    post_user_id = post_user_id_column["user_id"]
    if post_user_id == user_id:

        post_like = db.query(Like).filter(Like.post_id == post_id).all()
        for i in post_like:
            db.delete(i)

        post_to_delete = filter_query(db, post_id)
        db.delete(post_to_delete)
        db.commit()

        return {"data": post_to_delete, "message": "Post delete successfully"}
    return "Sorry! You can't delete the post."


def filter_query(db, id):

    return db.query(Post).filter(Post.id == id).first()
