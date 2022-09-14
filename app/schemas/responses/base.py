import datetime

from pydantic import BaseModel, Field


__all__ = [
    'UpdatedAtField',
    'CreatedAtField',
]


class UpdatedAtField(BaseModel):
    updated_at: datetime.datetime = Field(
        default=...,
        title='Дата/Время последнего обновления',
    )


class CreatedAtField(BaseModel):
    created_at: datetime.datetime = Field(
        default=...,
        title='Дата/Время последнего создания',
    )
