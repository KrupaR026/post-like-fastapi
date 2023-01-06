from server.database import Base
from sqlalchemy import Column, String
from server.utils.util import common_db_field


class User(common_db_field, Base):
    """crete the user table"""

    __tablename__ = "users"
    username = Column(String, unique=True)
    email = Column(String, nullable=False)
