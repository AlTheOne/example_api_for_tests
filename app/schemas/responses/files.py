from typing import List

from pydantic import BaseModel, Field

from schemas.responses.base import CreatedAtField, UpdatedAtField


class FileListItemForResponse(
    UpdatedAtField,
    CreatedAtField,
    BaseModel,
):
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


class FileListForResponse(BaseModel):
    """
    Список файлов.
    """
    total: int = Field(
        default=...,
        title='Общее количество',
    )
    items: List[FileListItemForResponse] = Field(
        default=...,
        title='Список',
    )
