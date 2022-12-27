from sqlalchemy import Column, DateTime, String
import uuid
from sqlalchemy.dialects.postgresql import UUID
import getpass
import datetime

"""
comman columns of three table
"""


class common_db_field:
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime)
    created_by = Column(String, default=getpass.getuser)
    updated_by = Column(String, default=getpass.getuser)
