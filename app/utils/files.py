import uuid

from core.settings import STATIC_DIR


def generate_file_path(
        user_id: int,
        filename: str,
) -> str:
    return f'{STATIC_DIR}/{user_id}_{uuid.uuid4().hex}_{filename}'
