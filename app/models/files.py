from sqlalchemy import Column, DateTime, func, Integer, String

from db.db import Base


__all__ = [
    'Files',
]


class Files(Base):
    __tablename__ = 'files'

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, index=True, nullable=False)
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)

    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
