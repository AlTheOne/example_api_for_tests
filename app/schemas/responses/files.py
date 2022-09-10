import datetime
from typing import List

from pydantic import BaseModel, Field


class FileListItemForResponse(BaseModel):
    """
    Элемент списка файлов.
    """
    id: int = Field(
        default=...,
        title='ID',
    )
    user_id: int = Field(
        default=...,
        title='ID пользователя',
    )
    filename: str = Field(
        default=...,
        title='Название файла',
    )
    updated_at: datetime.datetime
    created_at: datetime.datetime


class FileListForResponse(BaseModel):
    """
    Список файлов.
    """
    total: int = Field(
        default=...,
        title='Общее количество',
    )
    items: List[FileListItemForResponse]
