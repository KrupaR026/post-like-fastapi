from fastapi import APIRouter
from server.models.post_model import Post
from server.models.like_model import Like
from server.database.database import SessionLocal
from server.schemas.like_schemas import LikeBase


likeRouter = APIRouter()
db = SessionLocal()

@likeRouter.post('/like_the_post')
def like_the_post(like: LikeBase):
    """like the post by post id and user id

    Args:
        like (LikeBase): _description_

    Returns:
        _type_: _description_
    """    
    new_like = Like(
        post_id = like.post_id,
        user_id = like.user_id,
        username = like.userrname,
    )

    db_like = db.query(Like).filter(Like.user_id == like.user_id, Like.post_id == like.post_id).first()

    if db_like is not None:
        return 'You have alredy like the post'
    else:
        db.add(new_like)
        db.commit()
        total_like_column = db.query(Post.total_like).filter(Post.id == like.post_id).first()
        count = total_like_column["total_like"]
        count = count + 1
        db.query(Post).filter(Post.id == like.post_id).update({'total_like': count})
        db.commit()
        id = new_like.post_id
        return db.query(Post).filter(Post.id == id).first()


@likeRouter.get('/like_count/{post_id}')
def count_the_like(post_id: str):
    """count the total like of given post id

    Args:
        post_id (str): _description_

    Returns:
        _type_: _description_
    """    

    total_likes = db.query(Like).filter(Like.post_id == post_id).count()
    return total_likes


@likeRouter.get('/likes_user_details/{post_id}')
def post_details(post_id: str):
    """post like user details

    Args:
        post_id (str): _description_

    Returns:
        _type_: _description_
    """    
    like = db.query(Like).filter(Like.post_id == post_id).all()
    return like