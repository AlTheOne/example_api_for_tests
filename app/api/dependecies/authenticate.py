from typing import Optional

from fastapi import HTTPException
from jwt import ExpiredSignatureError
from starlette import status as http_status
from starlette.requests import Request

from core.settings import JWT_PREFIX_TOKEN
from schemas.jwt import AccessTokenPayload
from utils.jwt import get_jwt_token_payload


def _check_headers(request: Request) -> Optional[str]:
    """
    Проверка заголовка `Authorization` и данных в нём.

    :return: Токен, при наличии.
    """
    authorization_header: Optional[str] = request.headers.get('authorization')

    if authorization_header:
        try:
            prefix, token = authorization_header.split()
        except ValueError:
            raise HTTPException(status_code=http_status.HTTP_401_UNAUTHORIZED)

        if prefix != JWT_PREFIX_TOKEN or not token:
            raise HTTPException(status_code=http_status.HTTP_401_UNAUTHORIZED)

    else:
        token = None

    return token


def _get_payload(token: Optional[str]) -> AccessTokenPayload:
    """
    Расшифровка полезной нагрузки.
    Определение нагрузки (типа пользователя: ГОСТЬ/НЕ ГОСТЬ).

    :param token: ACCESS токен.

    :return: Сериализованная нагрузка.
    """
    if token:
        try:
            payload: AccessTokenPayload = AccessTokenPayload(**get_jwt_token_payload(
                jwt_token=token,
            ))
        except ExpiredSignatureError:
            raise HTTPException(status_code=http_status.HTTP_401_UNAUTHORIZED)

    else:
        raise HTTPException(status_code=http_status.HTTP_401_UNAUTHORIZED)

    return payload


def _get_current_user(
        request: Request,
) -> AccessTokenPayload:
    token: Optional[str] = _check_headers(request=request)
    payload_serialize_data: AccessTokenPayload = _get_payload(token=token)
    return payload_serialize_data


def get_current_user():
    def _get_func(request: Request) -> AccessTokenPayload:
        return _get_current_user(request=request)

    return _get_func
