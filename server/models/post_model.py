from server.database.database import Base
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from server.models.user_model import User


"""
create the datetime function
"""
def date_time():
    return datetime.utcnow()


"""
crete the post table
"""

class  Post(Base):
    __tablename__ = "post"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    title = Column(String)
    description = Column(String)
    published_at = Column(DateTime, default=date_time())
    updated_at = Column(DateTime, default=date_time())
    user_id = Column(UUID, ForeignKey(User.id))