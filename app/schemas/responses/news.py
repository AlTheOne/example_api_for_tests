from typing import List

from pydantic import BaseModel, Field

from schemas.responses.base import CreatedAtField, UpdatedAtField


class NewsListItemForResponse(BaseModel):
    """
    Элемент списка новостей.
    """
    id: int = Field(
        default=...,
        title='ID',
    )
    title: str = Field(
        default=...,
        title='Заголовок',
    )
    description: str = Field(
        default=...,
        title='Краткое описание',
    )


class NewsListForResponse(BaseModel):
    """
    Список новостей.
    """
    total: int = Field(
        default=...,
        title='Общее количество новостей',
    )
    items: List[NewsListItemForResponse] = Field(
        default=...,
        title='Новости',
    )


class NewsRetrieveForResponse(
    UpdatedAtField,
    CreatedAtField,
    BaseModel,
):
    """
    Новость.
    """
    id: int = Field(
        default=...,
        title='ID',
    )
    title: str = Field(
        default=...,
        title='Заголовок',
    )
    description: str = Field(
        default=...,
        title='Краткое описание',
    )
    content: str = Field(
        default=...,
        title='Содержимое',
    )
    is_active: bool = Field(
        default=...,
        title='Активно',
    )
