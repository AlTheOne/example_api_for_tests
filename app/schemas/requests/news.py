from typing import Optional

from fastapi import HTTPException
from fastapi import status as http_status
from pydantic import BaseModel, Field, root_validator

from resources import strings


class CreateNewsInRequest(BaseModel):
    """
    Создать новость.
    """
    title: Optional[str] = Field(
        default=...,
        title='Заголовок',
    )
    description: Optional[str] = Field(
        default=...,
        title='Краткое описание',
    )
    content: Optional[str] = Field(
        default=...,
        title='Содержимое',
    )

    is_active: Optional[bool] = Field(
        default=None,
        title='Новость доступна для просмотра',
    )


class PartialUpdateNewsInRequest(BaseModel):
    """
    Изменить новость.
    """
    title: Optional[str] = Field(
        default=None,
        title='Заголовок',
    )
    description: Optional[str] = Field(
        default=None,
        title='Краткое описание',
    )
    content: Optional[str] = Field(
        default=None,
        title='Содержимое',
    )

    is_active: Optional[bool] = Field(
        default=None,
        title='Новость доступна для просмотра',
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
