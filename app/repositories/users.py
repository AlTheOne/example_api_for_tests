from typing import List, Optional

from sqlalchemy.exc import IntegrityError

from db.exceptions import NonUniqueDataException, NotFoundDataException
from models.users import Users
from repositories.base import BaseRepository


__all__ = [
    'UsersRepository',
]


class UsersRepository(BaseRepository):
    table = Users

    def get_count(self) -> int:
        return self.connection.query(self.table).count()

    def get_list(
            self,
            offset: int = 0,
            limit: int = 100,
    ) -> List[Users]:
        return self.connection.query(self.table).offset(offset).limit(limit).all()

    def get(
            self,
            user_id: Optional[int] = None,
            phone: Optional[str] = None,
    ) -> Users:
        q = self.connection.query(self.table)
        if user_id is not None:
            q = q.filter(self.table.id == user_id)
        if phone is not None:
            q = q.filter(self.table.phone == phone)

        value = q.first()

        if value is None:
            raise NotFoundDataException

        return value

    def create(
            self,
            phone: str,
            first_name: str,
            last_name: str,
            middle_name: str,
            hashed_password: str,
            hashed_salt: str,
    ) -> Users:
        db_user = self.table(
            phone=phone,
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            is_active=True,
            hashed_password=hashed_password,
            hashed_salt=hashed_salt,
        )
        self.connection.add(db_user)

        try:
            self.connection.commit()
        except IntegrityError as e:
            self.connection.rollback()
            raise NonUniqueDataException(e)
        else:
            self.connection.refresh(db_user)

        return db_user

    def update(
            self,
            db_user: Users,
            first_name: Optional[str] = None,
            last_name: Optional[str] = None,
            middle_name: Optional[str] = None,
    ) -> Users:
        update_data = {}
        if first_name is not None:
            update_data['first_name'] = first_name
        if last_name is not None:
            update_data['last_name'] = last_name
        if middle_name is not None:
            update_data['middle_name'] = middle_name

        try:
            self.connection.query(self.table).filter(self.table.id == db_user.id).update(update_data)
        except IntegrityError as e:
            self.connection.rollback()
            raise NonUniqueDataException(e)
        else:
            self.connection.commit()

        return db_user
