from sqlalchemy import Boolean, Column, DateTime, func, Integer, String

from db.db import Base


__all__ = [
    'Users',
]


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String, unique=True, index=True, nullable=False)

    hashed_password = Column(String)
    hashed_salt = Column(String)

    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    middle_name = Column(String, nullable=False)

    is_active = Column(Boolean, nullable=False)

    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
