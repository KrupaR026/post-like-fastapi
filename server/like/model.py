from server.database import Base
from sqlalchemy import Column, ForeignKey, DateTime
from server.user.model import User
from server.post.model import Post
from sqlalchemy.dialects.postgresql import UUID
import uuid
import datetime


class Like(Base):
    """create the like table"""

    __tablename__ = "like"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    post_id = Column(UUID, ForeignKey(Post.id))
    like_by = Column(UUID, ForeignKey(User.id))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
