from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi import status as http_status

from api.dependecies.authenticate import get_current_user
from api.dependecies.database import get_repository
from db.exceptions import NonUniqueDataException, NotFoundDataException
from repositories.users import UsersRepository
from resources import strings
from schemas.jwt import AccessTokenPayload
from schemas.requests.users import (
    AuthUserInRequest,
    CreateUserInRequest,
    PartialUpdateUserInRequest,
)
from schemas.responses.users import AuthResponse, UserRetrieveForResponse
from utils.jwt import create_tokens
from utils.pswd import authentication


__all__ = [
    'prefix_router',
    'router',
]

prefix_router = 'users'
router = APIRouter()


@router.post(
    '/auth/',
    name=f'{prefix_router}:auth',
    response_model=AuthResponse,
    responses={
        int(http_status.HTTP_200_OK): {'description': 'User updated'},
        int(http_status.HTTP_400_BAD_REQUEST): {
            'description': strings.INVALID_PHONE_OR_PASSWORD_ERROR,
        },
    },
)
async def auth(
        request_data: AuthUserInRequest,
        users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
) -> AuthResponse:
    try:
        db_user = users_repo.get(phone=request_data.phone)
    except NotFoundDataException:
        raise HTTPException(
            status_code=http_status.HTTP_400_BAD_REQUEST,
            detail=strings.INVALID_PHONE_OR_PASSWORD_ERROR,
        )

    if not authentication(
            password=request_data.password,
            salt=db_user.hashed_salt,
            hashed_password=db_user.hashed_password,
    ):
        raise HTTPException(
            status_code=http_status.HTTP_400_BAD_REQUEST,
            detail=strings.INVALID_PHONE_OR_PASSWORD_ERROR,
        )

    tokens = create_tokens(
        payload={
            'user_id': db_user.id,
            'phone': db_user.phone,
        },
    )

    return AuthResponse(
        access_token=tokens[0],
        refresh_token=tokens[1],
        user=db_user.__dict__,
    )


@router.post(
    '/',
    name=f'{prefix_router}:create',
    responses={
        int(http_status.HTTP_201_CREATED): {'description': 'User created'},
        int(http_status.HTTP_400_BAD_REQUEST): {'description': strings.NON_UNIQUE_PHONE_ERROR},
    },
    status_code=http_status.HTTP_201_CREATED,
)
async def create(
        request_data: CreateUserInRequest,
        users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
) -> Response:
    try:
        users_repo.create(**request_data.get_data_for_create())
    except NonUniqueDataException:
        raise HTTPException(
            status_code=http_status.HTTP_400_BAD_REQUEST,
            detail=strings.NON_UNIQUE_PHONE_ERROR,
        )

    return Response(status_code=http_status.HTTP_201_CREATED)


@router.patch(
    '/',
    name=f'{prefix_router}:partial_update',
    response_model=UserRetrieveForResponse,
    responses={
        int(http_status.HTTP_200_OK): {'description': 'User updated'},
        int(http_status.HTTP_400_BAD_REQUEST): {'description': strings.INVALID_DATA_ERROR},
        int(http_status.HTTP_401_UNAUTHORIZED): {'description': strings.NOT_AUTH_ERROR},
        int(http_status.HTTP_404_NOT_FOUND): {'description': strings.USER_DOES_NOT_EXISTS_ERROR},
    },
)
async def partial_update(
        request_data: PartialUpdateUserInRequest,
        current_user: AccessTokenPayload = Depends(get_current_user()),
        users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
) -> UserRetrieveForResponse:
    try:
        db_user = users_repo.get(user_id=current_user.user_id)
    except NotFoundDataException:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND,
            detail=strings.USER_DOES_NOT_EXISTS_ERROR,
        )

    try:
        users_repo.update(
            db_user=db_user,
            **request_data.dict(exclude_none=True),
        )
    except Exception:
        raise HTTPException(
            status_code=http_status.HTTP_400_BAD_REQUEST,
            detail=strings.INVALID_DATA_ERROR,
        )

    db_user = users_repo.get(user_id=current_user.user_id)
    return UserRetrieveForResponse(**db_user.__dict__)
