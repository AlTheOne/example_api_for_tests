from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.routes import router as api_router
from core import settings
from core.events import create_start_app_handler, create_stop_app_handler
from db.db import engine
from models import news


def get_application() -> FastAPI:
    news.Base.metadata.create_all(bind=engine)

    application = FastAPI(
        title=settings.PROJECT_NAME,
        debug=settings.DEBUG,
        version=settings.VERSION,
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    application.add_event_handler(
        event_type='startup',
        func=create_start_app_handler(application),
    )
    application.add_event_handler(
        event_type='shutdown',
        func=create_stop_app_handler(application),
    )

    application.include_router(api_router, prefix=settings.API_PREFIX)

    return application


app = get_application()
