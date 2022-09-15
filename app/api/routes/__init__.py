from fastapi import APIRouter

from api.routes.files import prefix_router as files_prefix_router, router as files_router_v1
from api.routes.news import prefix_router as news_prefix_router, router as news_router_v1
from api.routes.users import prefix_router as users_prefix_router, router as users_router_v1


__all__ = [
    'router',
]

router = APIRouter(tags=['API'])
router.include_router(
    files_router_v1,
    tags=['V1', files_prefix_router],
    prefix=f'/v1/{files_prefix_router}',
)
router.include_router(
    news_router_v1,
    tags=['V1', news_prefix_router],
    prefix=f'/v1/{news_prefix_router}',
)
router.include_router(
    users_router_v1,
    tags=['V1', users_prefix_router],
    prefix=f'/v1/{users_prefix_router}',
)
