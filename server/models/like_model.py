from server.database.database import Base
from sqlalchemy import Column, ForeignKey, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from server.models.user_model import User
from server.models.post_model import Post


"""
create the like table
"""
class Like(Base):
    __tablename__ = "like"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    post_id = Column(UUID, ForeignKey(Post.id))
    user_id = Column(UUID, ForeignKey(User.id))
    username = Column(String)
    time = Column(DateTime, default=datetime.utcnow())
