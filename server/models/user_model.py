from server.database.database import Base
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

"""
create the datetime function
"""
def date_time():
    return datetime.utcnow()


"""
crete the user table
"""
class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    username = Column(String, unique = True)
    email = Column(String, nullable = False)
    created_at = Column(DateTime, default=date_time())
    updated_at = Column(DateTime, default=date_time())