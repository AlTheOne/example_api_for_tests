from fastapi import FastAPI

from db.db import SessionLocal


async def connect_to_db(app: FastAPI) -> None:
    app.state.pool = SessionLocal()


async def close_db_connection(app: FastAPI) -> None:
    app.state.pool.close()
