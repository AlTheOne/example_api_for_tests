import datetime
from typing import Any, Dict, Tuple

import jwt

from core import settings


def create_jwt_token(
        *,
        payload: Dict[str, str],
        secret_key: str,
        expires_delta: datetime.timedelta,
        subject: str,
) -> dict:
    """
    Создание JWT токена.

    :param payload: Полезная нагрузка.
    :param secret_key: Секретный ключ.
    :param expires_delta: Время жизни.
    :param subject: Тема токена (для чего).

    :return:
    """
    payload_to_encode = payload.copy()
    expire = datetime.datetime.utcnow() + expires_delta

    payload_to_encode.update({
        'exp': expire,
        'sub': subject,
    })

    token = jwt.encode(
        payload=payload_to_encode,
        key=secret_key,
        algorithm=settings.JWT_ALGORITHM,
    )

    return {
        'exp': expire,
        'sub': subject,
        'token': token,
    }


def create_access_jwt_token(payload: Dict[str, str]) -> dict:
    """
    Создание ACCESS токена.

    :param payload: Полезная нагрузка.
        Например, все данные пользователя для профиля.

    :return: Данные токена.
    """
    return create_jwt_token(
        payload=payload,
        secret_key=settings.JWT_SECRET_KEY,
        expires_delta=datetime.timedelta(minutes=5),
        subject=settings.JWT_ACCESS_SUBJECT,
    )


def create_refresh_jwt_token(payload: Dict[str, str]) -> dict:
    """
    Создание REFRESH токена.

    :param payload: Полезная нагрузка.
        Например, ID пользователя или статус.

    :return: Данные токена.
    """
    return create_jwt_token(
        payload=payload,
        secret_key=settings.JWT_SECRET_KEY,
        expires_delta=datetime.timedelta(minutes=60),
        subject=settings.JWT_REFRESH_SUBJECT,
    )


def create_tokens(payload: Dict[str, str]) -> Tuple[dict, dict]:
    """
    Создание ACCESS и REFRESH токенов.

    :param payload: Полезная нагрузка.

    :return: Данные токенов.
    """
    access_token = create_access_jwt_token(payload)
    refresh_token = create_refresh_jwt_token(payload)
    return access_token, refresh_token


def check_token_expires(created_at: datetime.datetime) -> bool:
    """
    Проверка срока годности REFRESH токена.

    :param created_at: Дата создания токена.

    :return: Токен скоро закончится. Нужно сгенерировать новый.
    """
    expires_in = datetime.datetime.utcnow() - created_at
    return datetime.timedelta(minutes=55) <= expires_in < datetime.timedelta(minutes=60)


def get_jwt_token_payload(jwt_token: str) -> Any:
    """
    Получить полезную нагрузку из JWT токена.

    :param jwt_token: Токен.

    :return: Полезная нагрузка.
    """
    return jwt.decode(
        jwt=jwt_token,
        key=settings.JWT_SECRET_KEY,
        algorithms=settings.JWT_ALGORITHM,
    )
