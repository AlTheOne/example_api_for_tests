from sqlalchemy import Boolean, Column, DateTime, func, Integer, String, Text

from db.db import Base


__all__ = [
    'News',
]


class News(Base):
    __tablename__ = 'news'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True)
    description = Column(String)
    content = Column(Text)
    is_active = Column(Boolean, default=True)

    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
