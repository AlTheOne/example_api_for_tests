import datetime
from typing import List

from pydantic import BaseModel, Field

from schemas.responses.base import CreatedAtField, UpdatedAtField


class UserListItemForResponse(BaseModel):
    """
    Элемент списка пользователей.
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
    items: List[UserListItemForResponse] = Field(
        default=...,
        title='Пользователи',
    )


class UserRetrieveForResponse(
    UpdatedAtField,
    CreatedAtField,
    BaseModel,
):
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
    is_active: bool


class TokenUserData(UserRetrieveForResponse):
    """Данные пользователя"""


class Token(BaseModel):
    exp: datetime.datetime
    sub: str
    token: str


class AuthResponse(BaseModel):
    access_token: Token
    refresh_token: Token
    user: TokenUserData
