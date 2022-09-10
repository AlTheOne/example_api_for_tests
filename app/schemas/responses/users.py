import datetime
from typing import List

from pydantic import BaseModel, Field


class UserListItemForResponse(BaseModel):
    """
    Пользователь.
    """
    id: int = Field(
        default=...,
        title='ID',
    )
    phone: str = Field(
        default=...,
        title='Номер телефона',
    )
    first_name: str = Field(
        default=...,
        title='Имя',
    )
    last_name: str = Field(
        default=...,
        title='Фамилия',
    )
    middle_name: str = Field(
        default=...,
        title='Отчество',
    )


class UserListForResponse(BaseModel):
    """
    Список пользователей.
    """
    total: int = Field(
        default=...,
        title='Общее количество',
    )
    items: List[UserListItemForResponse]


class UserRetrieveForResponse(BaseModel):
    """
    Пользователь.
    """
    id: int
    phone: str
    first_name: str
    last_name: str
    middle_name: str
    is_active: bool
    updated_at: datetime.datetime
    created_at: datetime.datetime
