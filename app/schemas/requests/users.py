from typing import Optional

from fastapi import HTTPException
from fastapi import status as http_status
from pydantic import BaseModel, Field, root_validator

from resources import strings
from utils.pswd import generate_salt, get_password_hash


class AuthUserInRequest(BaseModel):
    """
    Создать пользователя.
    """
    phone: str = Field(
        default=...,
        title='Номер телефона',
    )
    password: str = Field(
        default=...,
        title='Пароль',
    )


class CreateUserInRequest(BaseModel):
    """
    Создать пользователя.
    """
    phone: str = Field(
        default=...,
        title='Номер телефона',
    )
    password: str = Field(
        default=...,
        title='Пароль',
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
        default='',
        title='Отчество',
    )

    def get_data_for_create(self) -> dict:
        data = self.dict(exclude={'password'})
        data['hashed_salt'] = generate_salt()
        data['hashed_password'] = get_password_hash(
            password=self.password,
            salt=data['hashed_salt'],
        )
        return data


class PartialUpdateUserInRequest(BaseModel):
    """
    Изменить пользователя.
    """
    first_name: Optional[str] = Field(
        default=None,
        title='Имя',
    )
    last_name: Optional[str] = Field(
        default=None,
        title='Фамилия',
    )
    middle_name: Optional[str] = Field(
        default=None,
        title='Отчество',
    )

    @root_validator()
    def check_fields(cls, values):
        for val in values.values():
            if val is not None:
                break
        else:
            raise HTTPException(
                status_code=http_status.HTTP_400_BAD_REQUEST,
                detail=strings.NO_DATA_TO_UPDATE_ERROR,
            )

        return values
