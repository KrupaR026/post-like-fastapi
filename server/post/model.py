from server.database import Base
from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from server.user.model import User
from server.utils.util import common_db_field


"""
crete the post table
"""

class  Post(common_db_field, Base):
    __tablename__ = "post"
    title = Column(String)
    description = Column(String)
    user_id = Column(UUID, ForeignKey(User.id))
    total_like = Column(Integer, default = 0)