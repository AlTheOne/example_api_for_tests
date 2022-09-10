import datetime
from typing import List

from pydantic import BaseModel, Field


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
    items: List[NewsListItemForResponse]


class NewsRetrieveForResponse(BaseModel):
    """
    Новость.
    """
    id: int
    title: str
    description: str
    content: str
    is_active: bool
    updated_at: datetime.datetime
    created_at: datetime.datetime
