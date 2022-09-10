from typing import List, Optional

from sqlalchemy.exc import IntegrityError

from db.exceptions import NonUniqueDataException, NotFoundDataException
from models.news import News
from repositories.base import BaseRepository


__all__ = [
    'NewsRepository',
]


class NewsRepository(BaseRepository):
    table = News

    def get_count(self) -> int:
        return self.connection.query(self.table).count()

    def get_list(
            self,
            offset: int = 0,
            limit: int = 100,
            is_active: Optional[bool] = None,
    ) -> List[News]:
        q = self.connection.query(self.table)

        if is_active is not None:
            q = q.filter(self.table.is_active == is_active)

        q = q.offset(offset).limit(limit)
        values = q.all()

        return values

    def get(
            self,
            news_id: int,
    ) -> News:
        value = self.connection.query(self.table).filter(self.table.id == news_id).first()
        if value is None:
            raise NotFoundDataException

        return value

    def create(
            self,
            title: str,
            description: str,
            content: str,
            is_active: bool,
    ) -> News:
        db_news = self.table(
            title=title,
            description=description,
            content=content,
            is_active=is_active,
        )
        self.connection.add(db_news)

        try:
            self.connection.commit()
        except IntegrityError as e:
            self.connection.rollback()
            raise NonUniqueDataException(e)
        else:
            self.connection.refresh(db_news)

        return db_news

    def update(
            self,
            db_news: News,
            title: Optional[str] = None,
            description: Optional[str] = None,
            content: Optional[str] = None,
            is_active: Optional[bool] = None,
    ) -> News:
        update_data = {}
        if title is not None:
            update_data['title'] = title
        if description is not None:
            update_data['description'] = description
        if content is not None:
            update_data['content'] = content
        if is_active is not None:
            update_data['is_active'] = is_active

        try:
            self.connection.query(self.table).filter(
                self.table.id == db_news.id,
            ).update(update_data)
        except IntegrityError as e:
            self.connection.rollback()
            raise NonUniqueDataException(e)
        else:
            self.connection.commit()

        return db_news

    def delete(
            self,
            news_id: int,
    ) -> None:
        self.connection.query(self.table).filter(self.table.id == news_id).delete()
        self.connection.commit()
