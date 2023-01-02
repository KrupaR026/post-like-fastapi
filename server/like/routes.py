from fastapi import APIRouter, Depends
from server.user.model import User
from server.post.model import Post
from server.like.model import Like
from server.like.schemas import LikeBase
from server.database import get_db
from sqlalchemy.orm import Session


likeRouter = APIRouter()


def db_like_function(db, like: LikeBase):
    return (
        db.query(Like)
        .filter(Like.user_id == like.user_id, Like.post_id == like.post_id)
        .first()
    )


def total_like_column_function(db, like: LikeBase):
    total_like_column = (
        db.query(Post.total_like).filter(Post.id == like.post_id).first()
    )
    count = total_like_column["total_like"]
    count = count + 1
    db.query(Post).filter(Post.id == like.post_id).update({"total_like": count})


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

    def post_like_function(db, like: LikeBase):
        db_like = (
            db.query(Like)
            .filter(Like.user_id == like.user_id, Like.post_id == like.post_id)
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
            count = count + 1
            db.query(Post).filter(Post.id == like.post_id).update({"total_like": count})
            db.commit()
            id = new_like.post_id
            return db.query(Post).filter(Post.id == id).first()

    two_post_column = (
        db.query(Post.post_type, Post.post_display_user)
        .filter(Post.id == new_like.post_id)
        .first()
    )
    public_or_private = two_post_column["post_type"]
    post_user_id_filed = (
        db.query(Post.user_id).filter(Post.id == new_like.post_id).first()
    )
    post_user_id = post_user_id_filed["user_id"]

    if public_or_private == "public":
        return post_like_function(db, new_like)

    elif public_or_private == "private":
        if new_like.user_id == post_user_id:
            return post_like_function(db, new_like)
        else:
            return "Sorry, This post is private. So you can't see and like it."

    else:
        display_all_users = two_post_column["post_display_user"]
        display_user_list = display_all_users.split()
        if new_like.user_id in display_user_list or new_like.user_id == post_user_id:
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

    total_likes = db.query(Like).filter(Like.post_id == post_id).count()
    return total_likes


@likeRouter.get("/likes_user_details/{post_id}/{user_id}")
def post_details(post_id: str, user_id: str, db: Session = Depends(get_db)):
    """post like user details

    Args:
        post_id (str): _description_

    Returns:
        _type_: _description_
    """

    post_user_id_column = db.query(Post.user_id).filter(Post.id == post_id).first()
    post_user_id = post_user_id_column["user_id"]
    if post_user_id == user_id:
        likes_user_id_filed = (
            db.query(Like.user_id).filter(Like.post_id == post_id).all()
        )

        like_user_id_list = []
        for i in range(len(likes_user_id_filed)):
            likes_user_id = likes_user_id_filed[i]["user_id"]
            like_user_id_list.append(likes_user_id)

        user_details_list = []
        for j in like_user_id_list:
            user_details = db.query(User).filter(User.id == j).first()
            user_details_list.append(user_details)

        return user_details_list

    else:
        return "Sorry! You can't see the likes user details."


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
    if dislike is None:
        return "Sorry! You can't dislike the post as you haven't liked it earlier."
    else:
        db.delete(dislike)
        db.commit()

        total_like_column = db.query(Post.total_like).filter(Post.id == post_id).first()
        count = total_like_column["total_like"]
        count = count - 1
        db.query(Post).filter(Post.id == post_id).update({"total_like": count})
        db.commit()

        post = db.query(Post).filter(Post.id == post_id).first()
        return {"data": post, "message": "You dislike the above post"}
