from server.database import Base
from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from server.user.model import User
from server.post.model import Post
from server.utils.util import common_db_field

"""
create the like table
"""
class Like(common_db_field, Base):
    __tablename__ = "like"
    post_id = Column(UUID, ForeignKey(Post.id))
    user_id = Column(UUID, ForeignKey(User.id))
