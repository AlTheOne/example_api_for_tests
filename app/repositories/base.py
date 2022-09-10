from sqlalchemy.orm import Session


class BaseRepository:
    def __init__(self, conn: Session) -> None:
        self._conn = conn

    @property
    def connection(self) -> Session:
        return self._conn
