import io
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi import status as http_status
from fastapi import UploadFile
from fastapi.responses import StreamingResponse

from api.dependecies.authenticate import get_current_user
from api.dependecies.database import get_repository
from db.exceptions import NotFoundDataException
from repositories.files import FilesRepository
from resources import strings
from schemas.jwt import AccessTokenPayload
from schemas.responses.files import FileListForResponse, FileListItemForResponse
from utils.files import generate_file_path


__all__ = [
    'prefix_router',
    'router',
]

prefix_router = 'files'
router = APIRouter()


@router.get(
    '/',
    name=f'{prefix_router}:list',
    response_model=FileListForResponse,
    responses={
        int(http_status.HTTP_200_OK): {'description': 'OK'},
        int(http_status.HTTP_401_UNAUTHORIZED): {'description': strings.NOT_AUTH_ERROR},
    },
)
async def get_list(
        limit: int = Query(
            10,
            ge=1,
            le=20,
            description='Количество элементов в выдаче',
        ),
        offset: int = Query(
            0,
            ge=0,
            description='Сдвиг по списку',
        ),
        user_id: Optional[int] = None,
        _: AccessTokenPayload = Depends(get_current_user()),
        file_repo: FilesRepository = Depends(get_repository(FilesRepository)),
) -> FileListForResponse:
    db_count = file_repo.get_count()
    db_files = file_repo.get_list(
        limit=limit,
        offset=offset,
        user_id=user_id,
    )

    return FileListForResponse(
        total=db_count,
        items=[FileListItemForResponse(**db_file.__dict__) for db_file in db_files],
    )


@router.post(
    '/upload/',
    name=f'{prefix_router}:upload',
    response_model=FileListItemForResponse,
    responses={
        int(http_status.HTTP_200_OK): {'description': 'File uploaded'},
        int(http_status.HTTP_400_BAD_REQUEST): {'description': strings.NON_UNIQUE_TITLE_ERROR},
        int(http_status.HTTP_401_UNAUTHORIZED): {'description': strings.NOT_AUTH_ERROR},
    },
)
async def upload_file(
        file: UploadFile,
        current_user: AccessTokenPayload = Depends(get_current_user()),
        file_repo: FilesRepository = Depends(get_repository(FilesRepository)),
) -> FileListItemForResponse:
    file_path = generate_file_path(
        user_id=current_user.user_id,
        filename=file.filename,
    )

    db_file = file_repo.create(
        user_id=current_user.user_id,
        filename=file.filename,
        file_path=file_path,
    )

    with open(file_path, mode='wb') as f:
        f.write(file.file.read())

    return FileListItemForResponse(**db_file.__dict__)


@router.get(
    '/download/',
    name=f'{prefix_router}:download',
    responses={
        int(http_status.HTTP_200_OK): {
            'description': 'File download',
            'content': {'application/octet-stream': {}},
        },
        int(http_status.HTTP_400_BAD_REQUEST): {'description': strings.NON_UNIQUE_TITLE_ERROR},
        int(http_status.HTTP_401_UNAUTHORIZED): {'description': strings.NOT_AUTH_ERROR},
        int(http_status.HTTP_404_NOT_FOUND): {'description': strings.FILE_DOES_NOT_EXISTS_ERROR},
    },
)
async def download_file(
        file_id: int,
        _: AccessTokenPayload = Depends(get_current_user()),
        file_repo: FilesRepository = Depends(get_repository(FilesRepository)),
) -> StreamingResponse:
    try:
        db_file = file_repo.get(file_id=file_id)
    except NotFoundDataException:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND,
            detail=strings.FILE_DOES_NOT_EXISTS_ERROR,
        )

    with open(db_file.file_path, mode='rb') as f:
        return StreamingResponse(
            content=io.BytesIO(f.read()),
            headers={
                'Content-Disposition': f'inline; filename="{db_file.filename}"',
            },
        )
