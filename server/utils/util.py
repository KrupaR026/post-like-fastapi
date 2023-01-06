from sqlalchemy import Column, DateTime, Boolean
import uuid
from sqlalchemy.dialects.postgresql import UUID
import datetime


class common_db_field:
    """comman columns of three table"""

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(
        DateTime, onupdate=datetime.datetime.utcnow, default=datetime.datetime.utcnow
    )
    is_delete = Column(Boolean, default=False)
