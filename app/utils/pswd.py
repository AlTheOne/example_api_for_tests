import base64
import hashlib
import os


def get_password_hash(
        password: str,
        salt: str,
) -> str:
    """
    Получить хэш пароля.

    :param password: Пароль.
    :param salt: Соль.

    :return: Хэш пароля.
    """
    key = hashlib.pbkdf2_hmac(
        hash_name='sha256',
        password=password.encode('utf-8'),
        salt=base64.b64decode(salt),
        iterations=100000,
    )
    return base64.b64encode(key).decode()


def authentication(
        password: str,
        salt: str,
        hashed_password: str,
) -> bool:
    """
    Проверка пароля.

    :param password: Пароль, который нужно сравнить с хэшированным.
    :param salt: Соль.
    :param hashed_password: Хэшированный пароль.

    :return: Хэши паролей совпадают.
    """
    _hashed_password = get_password_hash(password=password, salt=salt)
    return _hashed_password == hashed_password


def generate_salt() -> str:
    return base64.b64encode(os.urandom(32)).decode()
