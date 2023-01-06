from server.database import Base
from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from server.user.model import User
from server.utils.util import common_db_field


class Post(common_db_field, Base):
    """crete the post table"""

    __tablename__ = "post"
    title = Column(String)
    description = Column(String)
    total_like = Column(Integer, default=0)
    post_type = Column(String)
    post_display_user = Column(String)
    created_by = Column(UUID, ForeignKey(User.id))
    updated_by = Column(UUID, ForeignKey(User.id))
