from fastapi import APIRouter, status, Depends, HTTPException
from server.post.schemas import PostBase, PostUpdate
from server.post.model import Post
from server.like.model import Like
from server.database import get_db
from sqlalchemy.orm import Session

postRouter = APIRouter()


@postRouter.post("/post", status_code=status.HTTP_201_CREATED)
def create_new_post(post: PostBase, user_id: str, db: Session = Depends(get_db)):
    """create the new post

    Args:
        post (PostBase): _description_

    Returns:
        _type_: _description_
    """
    new_post = Post(
        title=post.title,
        description=post.description,
        created_by=user_id,
        updated_by=user_id,
        post_type=post.post_type,
        post_display_user=post.post_display_user,
    )
    db.add(new_post)
    db.commit()

    print(new_post)
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
    post_to_update = filter_query(db, post_id).first()
    if post_to_update is not None:

        if post_to_update.is_delete == False:
            post_user_id_column = (
                db.query(Post.created_by).filter(Post.id == post_id).first()
            )
            post_user_id = post_user_id_column["created_by"]

            if post_user_id == user_id:
                post_dict = post.dict(exclude_unset=True)

                for key, value in post_dict.items():
                    setattr(post_to_update, key, value)

                db.commit()
                return {"message": "Post updated successfully"}
            else:
                return "You have no rights to update the post"

        else:
            return "This post has been deleted earlier so the data cannot be update."

    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@postRouter.get("/post", status_code=status.HTTP_404_NOT_FOUND)
def get_all_the_post_with_like_count(db: Session = Depends(get_db)):
    """get all the post with total likes and post details

    Returns:
        _type_: _description_
    """

    all_post = (
        db.query(Post).filter(Post.post_type == "public", Post.is_delete == False).all()
    )
    return all_post


@postRouter.get("/post/{post_id}/{user_id}")
def post_and_total_like(post_id: str, user_id: str, db: Session = Depends(get_db)):
    """get the post and total likes by specific post id

    Args:
        post_id (str): _description_

    Returns:
        _type_: _description_
    """
    post = filter_query(db, post_id).first()
    if post is not None:
        if post.is_delete == False:
            two_post_column = (
                db.query(Post.post_type, Post.post_display_user)
                .filter(Post.id == post_id)
                .first()
            )
            public_or_private = two_post_column["post_type"]

            if public_or_private == "public":
                return post

            else:

                display_user_list = two_post_column["post_display_user"].split()

                post_user_id_filed = (
                    db.query(Post.created_by).filter(Post.id == post_id).first()
                )
                post_user_id = post_user_id_filed["created_by"]

                if user_id in display_user_list or user_id == post_user_id:
                    return post
                else:
                    return "Sorry, This post is private. So you can't see it."
        else:
            return "This post has been deleted earlier so the data cannot be retrieved."

    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@postRouter.delete("/post/{post_id}/{user_id}")
def delete_post(post_id: str, user_id: str, db: Session = Depends(get_db)):
    """Delete method to delete a post by id

    Args:
        id (str): _description_

    Returns:
        _type_: _description_
    """
    post_to_delete = filter_query(db, post_id).first()
    if post_to_delete is not None:
        post_user_id_column = (
            db.query(Post.created_by).filter(Post.id == post_id).first()
        )
        post_user_id = post_user_id_column["created_by"]
        if post_user_id == user_id:

            post_like = db.query(Like).filter(Like.post_id == post_id).all()
            for i in post_like:
                db.delete(i)

            filter_query(db, post_id).update({"is_delete": True})
            db.commit()

            return {"data": post_to_delete, "message": "Post delete successfully"}
        return "Sorry! You can't delete the post."
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


def filter_query(db, id):

    return db.query(Post).filter(Post.id == id)
