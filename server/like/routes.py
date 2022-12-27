from fastapi import APIRouter, Depends
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
        user_id=like.user_id,
    )

    post_type = db.query(Post.post_type).filter(Post.id == new_like.post_id).first()
    public_or_private = post_type["post_type"]
    if public_or_private == "private":
        return "Sorry, This post is private. So you can't see and like it."
    else:
        db_like = (
            db.query(Like)
            .filter(Like.user_id == like.user_id, Like.post_id == like.post_id)
            .first()
        )
        if db_like is not None:
            return "You have already like the post"
        else:
            db.add(new_like)
            db.commit()
            total_like_column = (
                db.query(Post.total_like).filter(Post.id == like.post_id).first()
            )
            count = total_like_column["total_like"]
            count = count + 1
            db.query(Post).filter(Post.id == like.post_id).update({"total_like": count})
            db.commit()
            id = new_like.post_id
            return db.query(Post).filter(Post.id == id).first()


@likeRouter.get("/like_count/{post_id}")
def count_the_like(post_id: str, db: Session = Depends(get_db)):
    """count the total like of given post id

    Args:
        post_id (str): _description_

    Returns:
        _type_: _description_
    """

    total_likes = db.query(Like).filter(Like.post_id == post_id).count()
    return total_likes


@likeRouter.get("/likes_user_details/{post_id}")
def post_details(post_id: str, db: Session = Depends(get_db)):
    """post like user details

    Args:
        post_id (str): _description_

    Returns:
        _type_: _description_
    """
    like = db.query(Like).filter(Like.post_id == post_id).all()
    return like


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
        db.query(Like).filter(Like.post_id == post_id, Like.user_id == user_id).first()
    )
    db.delete(dislike)
    db.commit()

    total_like_column = db.query(Post.total_like).filter(Post.id == post_id).first()
    count = total_like_column["total_like"]
    count = count - 1
    db.query(Post).filter(Post.id == post_id).update({"total_like": count})
    db.commit()

    post = db.query(Post).filter(Post.id == post_id).first()
    return {"data": post, "message": "You dislike the above post"}
