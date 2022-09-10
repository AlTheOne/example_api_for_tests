from typing import List, Optional

from db.exceptions import NotFoundDataException
from models.files import Files
from repositories.base import BaseRepository


__all__ = [
    'FilesRepository',
]


class FilesRepository(BaseRepository):
    table = Files

    def get_count(self) -> int:
        return self.connection.query(self.table).count()

    def get_list(
            self,
            offset: int = 0,
            limit: int = 100,
            user_id: Optional[int] = None,
    ) -> List[Files]:
        q = self.connection.query(self.table)
        if user_id:
            q = q.filter(self.table.user_id == user_id)

        values = q.offset(offset).limit(limit).all()
        return values

    def get(
            self,
            file_id: int,
    ) -> Files:
        value = self.connection.query(self.table).filter(self.table.id == file_id).first()
        if value is None:
            raise NotFoundDataException

        return value

    def create(
            self,
            user_id: int,
            filename: str,
            file_path: str,
    ) -> Files:
        db_file = self.table(
            user_id=user_id,
            filename=filename,
            file_path=file_path,
        )
        self.connection.add(db_file)
        self.connection.commit()
        self.connection.refresh(db_file)

        return db_file
