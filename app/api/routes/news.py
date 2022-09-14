from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi import status as http_status

from api.dependecies.authenticate import get_current_user
from api.dependecies.database import get_repository
from db.exceptions import NonUniqueDataException, NotFoundDataException
from repositories.news import NewsRepository
from resources import strings
from schemas.jwt import AccessTokenPayload
from schemas.requests.news import CreateNewsInRequest, PartialUpdateNewsInRequest
from schemas.responses.news import (
    NewsListForResponse,
    NewsListItemForResponse,
    NewsRetrieveForResponse,
)


__all__ = [
    'prefix_router',
    'router',
]

prefix_router = 'news'
router = APIRouter()


@router.get(
    '/',
    name=f'{prefix_router}:get_list',
    response_model=NewsListForResponse,
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
        is_active: Optional[bool] = None,
        news_repo: NewsRepository = Depends(get_repository(NewsRepository)),
) -> NewsListForResponse:
    db_count = news_repo.get_count()
    db_news = news_repo.get_list(
        limit=limit,
        offset=offset,
        is_active=is_active,
    )

    return NewsListForResponse(
        total=db_count,
        items=[NewsListItemForResponse(**db_new.__dict__) for db_new in db_news],
    )


@router.get(
    '/{news_id}/',
    name=f'{prefix_router}:get_retrieve',
    response_model=NewsRetrieveForResponse,
)
async def get_retrieve(
        news_id: int,
        news_repo: NewsRepository = Depends(get_repository(NewsRepository)),
) -> NewsRetrieveForResponse:
    try:
        db_news = news_repo.get(news_id=news_id)
    except NotFoundDataException:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND,
            detail=strings.NEWS_DOES_NOT_EXISTS_ERROR,
        )

    return NewsRetrieveForResponse(**db_news.__dict__)


@router.post(
    '/',
    name=f'{prefix_router}:create',
    response_model=NewsRetrieveForResponse,
    responses={
        int(http_status.HTTP_201_CREATED): {'description': 'News created'},
        int(http_status.HTTP_400_BAD_REQUEST): {'description': strings.NON_UNIQUE_TITLE_ERROR},
        int(http_status.HTTP_401_UNAUTHORIZED): {'description': strings.NOT_AUTH_ERROR},
    },
    status_code=http_status.HTTP_201_CREATED,
)
async def create(
        request_data: CreateNewsInRequest,
        _: AccessTokenPayload = Depends(get_current_user()),
        news_repo: NewsRepository = Depends(get_repository(NewsRepository)),
) -> NewsRetrieveForResponse:
    try:
        db_news = news_repo.create(**request_data.dict())
    except NonUniqueDataException:
        raise HTTPException(
            status_code=http_status.HTTP_400_BAD_REQUEST,
            detail=strings.NON_UNIQUE_TITLE_ERROR,
        )

    return NewsRetrieveForResponse(**db_news.__dict__)


@router.patch(
    '/{news_id}/',
    name=f'{prefix_router}:partial_update',
    response_model=NewsRetrieveForResponse,
    responses={
        int(http_status.HTTP_200_OK): {'description': 'News updated'},
        int(http_status.HTTP_400_BAD_REQUEST): {'description': strings.INVALID_DATA_ERROR},
        int(http_status.HTTP_401_UNAUTHORIZED): {'description': strings.NOT_AUTH_ERROR},
        int(http_status.HTTP_404_NOT_FOUND): {'description': strings.NEWS_DOES_NOT_EXISTS_ERROR},
    },
)
async def partial_update(
        news_id: int,
        request_data: PartialUpdateNewsInRequest,
        _: AccessTokenPayload = Depends(get_current_user()),
        news_repo: NewsRepository = Depends(get_repository(NewsRepository)),
) -> NewsRetrieveForResponse:
    try:
        db_news = news_repo.get(news_id=news_id)
    except NotFoundDataException:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND,
            detail=strings.NEWS_DOES_NOT_EXISTS_ERROR,
        )

    try:
        news_repo.update(
            db_news=db_news,
            **request_data.dict(exclude_none=True),
        )
    except Exception:
        raise HTTPException(
            status_code=http_status.HTTP_400_BAD_REQUEST,
            detail=strings.INVALID_DATA_ERROR,
        )

    db_news = news_repo.get(news_id=news_id)
    return NewsRetrieveForResponse(**db_news.__dict__)


@router.put(
    '/{news_id}/',
    name=f'{prefix_router}:update',
    response_model=NewsRetrieveForResponse,
    responses={
        int(http_status.HTTP_200_OK): {'description': 'News updated'},
        int(http_status.HTTP_400_BAD_REQUEST): {'description': strings.NON_UNIQUE_TITLE_ERROR},
        int(http_status.HTTP_401_UNAUTHORIZED): {'description': strings.NOT_AUTH_ERROR},
        int(http_status.HTTP_404_NOT_FOUND): {'description': strings.NEWS_DOES_NOT_EXISTS_ERROR},
    },
)
async def update(
        news_id: int,
        request_data: PartialUpdateNewsInRequest,
        _: AccessTokenPayload = Depends(get_current_user()),
        news_repo: NewsRepository = Depends(get_repository(NewsRepository)),
) -> NewsRetrieveForResponse:
    try:
        db_news = news_repo.get(news_id=news_id)
    except NotFoundDataException:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND,
            detail=strings.NEWS_DOES_NOT_EXISTS_ERROR,
        )

    try:
        news_repo.update(
            db_news=db_news,
            **request_data.dict(),
        )
    except NonUniqueDataException:
        raise HTTPException(
            status_code=http_status.HTTP_400_BAD_REQUEST,
            detail=strings.NON_UNIQUE_TITLE_ERROR,
        )
    except Exception as e:
        raise HTTPException(
            status_code=http_status.HTTP_400_BAD_REQUEST,
            detail=strings.INVALID_DATA_ERROR,
        )

    db_news = news_repo.get(news_id=news_id)
    return NewsRetrieveForResponse(**db_news.__dict__)


@router.delete(
    '/{news_id}/',
    name=f'{prefix_router}:delete',
    response_model=NewsRetrieveForResponse,
)
async def delete(
        news_id: int,
        _: AccessTokenPayload = Depends(get_current_user()),
        news_repo: NewsRepository = Depends(get_repository(NewsRepository)),
) -> NewsRetrieveForResponse:
    try:
        db_news = news_repo.get(news_id=news_id)
    except NotFoundDataException:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND,
            detail=strings.NEWS_DOES_NOT_EXISTS_ERROR,
        )

    try:
        news_repo.delete(news_id=news_id)
    except Exception:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND,
            detail=strings.INVALID_DATA_ERROR,
        )

    return NewsRetrieveForResponse(**db_news.__dict__)
