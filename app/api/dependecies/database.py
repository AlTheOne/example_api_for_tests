from sqlite3 import Connection
from typing import Callable, Type

from fastapi import Depends, Request

from repositories.base import BaseRepository


def _get_db_pool(request: Request) -> Connection:
    return request.app.state.pool


def get_repository(
        repo_type: Type[BaseRepository],
) -> Callable[[Connection], BaseRepository]:
    def _get_repo(
            conn: Connection = Depends(_get_db_pool),
    ) -> BaseRepository:
        return repo_type(conn)

    return _get_repo
