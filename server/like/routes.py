from fastapi import APIRouter, Depends
from server.user.model import User
from server.post.model import Post
from server.like.model import Like
from server.like.schemas import LikeBase
from server.database import get_db
from sqlalchemy.orm import Session


likeRouter = APIRouter()


@likeRouter.post("/like_the_post")
def like_the_post(like: LikeBase, db: Session = Depends(get_db)):
    """like the post by post id and user id

    Args:
        like (LikeBase): _description_

    Returns:
        _type_: _description_
    """
    new_like = Like(
        post_id=like.post_id,
        like_by=like.like_by,
    )

    def post_like_function(db, like: LikeBase):
        db_like = (
            db.query(Like)
            .filter(Like.like_by == like.like_by, Like.post_id == like.post_id)
            .first()
        )
        if db_like is not None:
            return "You have already like the post"
        else:
            db.add(new_like)
            total_like_column = (
                db.query(Post.total_like).filter(Post.id == like.post_id).first()
            )
            count = total_like_column["total_like"]
            count += 1
            db.query(Post).filter(Post.id == like.post_id).update({"total_like": count})
            db.commit()

            return db.query(Post).filter(Post.id == new_like.post_id).first()

    two_post_column = (
        db.query(Post.post_type, Post.post_display_user)
        .filter(Post.id == new_like.post_id)
        .first()
    )
    public_or_private = two_post_column["post_type"]

    if public_or_private == "public":
        return post_like_function(db, new_like)

    else:
        post_user_id_filed = (
            db.query(Post.created_by).filter(Post.id == new_like.post_id).first()
        )
        post_user_id = post_user_id_filed["created_by"]

        display_user_list = two_post_column["post_display_user"].split()

        if new_like.like_by in display_user_list or new_like.like_by == post_user_id:
            return post_like_function(db, new_like)
        else:
            return "Sorry, This post is private. So you can't see and like it."


@likeRouter.get("/like_count/{post_id}")
def count_the_like(post_id: str, db: Session = Depends(get_db)):
    """count the total like of given post id

    Args:
        post_id (str): _description_

    Returns:
        _type_: _description_
    """

    total_like = db.query(Like).filter(Like.post_id == post_id).count()
    return total_like


@likeRouter.get("/likes_user_details/{post_id}/{user_id}")
def post_details(post_id: str, user_id: str, db: Session = Depends(get_db)):
    """post like user details

    Args:
        post_id (str): _description_

    Returns:
        _type_: _description_
    """

    post = db.query(Post.created_by, Post.is_delete).filter(Post.id == post_id).first()
    if post.is_delete == False:
        post_user_id = post["created_by"]
        if post_user_id == user_id:
            likes_user_id_filed = (
                db.query(Like.like_by).filter(Like.post_id == post_id).all()
            )

            like_user_id_list = [
                likes_user_id_filed[i]["like_by"]
                for i in range(len(likes_user_id_filed))
            ]
            user_details_list = [
                db.query(User).filter(User.id == i).first() for i in like_user_id_list
            ]
            return user_details_list

        else:
            return "Sorry! You can't see the likes user details."
    else:
        return "This post has been deleted earlier so the data cannot be retrieved details."


@likeRouter.delete("/dislike/{post_id}/{user_id}")
def dislike_the_post(post_id: str, user_id: str, db: Session = Depends(get_db)):
    """dislike the post using post_id and user_id

    Args:
        post_id (str): _description_
        user_id (str): _description_

    Returns:
        _type_: _description_
    """

    dislike = (
        db.query(Like).filter(Like.post_id == post_id, Like.like_by == user_id).first()
    )
    if dislike is None:
        return "Sorry! You can't dislike the post as you haven't liked it earlier."
    else:
        db.delete(dislike)
        db.commit()

        total_like_column = db.query(Post.total_like).filter(Post.id == post_id).first()
        count = total_like_column["total_like"]
        count -= 1
        db.query(Post).filter(Post.id == post_id).update({"total_like": count})
        db.commit()

        post = db.query(Post).filter(Post.id == post_id).first()
        return {"data": post, "message": "You dislike the above post"}
