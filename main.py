#!/bin/env python3

from contextlib import asynccontextmanager
import time
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter

from src.api.post import post_router, tag_router
from src.models.users import Role, User
from src.api.auth.auth import auth_router
from src.api.general.check import general_check_router
from src.api.transform_images import images_router
from src.api.comment import comments_router, admin_moderator_comments_router
from src.api.user import user_router, admin_moderator_work_with_user_router
from src.api.qrcode import qr_code_router
from src.db.redis import redis_manager
from src.repository.user import create_admin
from src.db.database import sessionmanager
from src.core import log
from src.core import base_config
from src.db import events
from src import genlib


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Lifespan function for managing the startup and shutdown lifecycle of the FastAPI application.

    This function is used to initialize and clean up the Redis connection and setup
    the FastAPILimiter during the application's lifespan. It connects to Redis
    when the app starts and closes the connection when the app shuts down.

    Args:
        app (FastAPI): The FastAPI application instance that will use this lifespan manager.

    Yields:
        None: This is a context manager, and the yielded value is unused. It simply
        marks the point where the application is running.

    Example:
        ```python
        app = FastAPI(lifespan=lifespan)
        ```
    """
    log.info("App starting up...")

    await redis_manager.connect()
    async with sessionmanager.session() as db:
        await create_admin(db)
    # Отримуємо сесію Redis для FastAPILimiter
    async with redis_manager.session() as redis:
        await FastAPILimiter.init(redis)

    yield
    log.info("App shutting down...")
    await redis_manager.close()
    await FastAPILimiter.close()


app = FastAPI(
    debug=True,
    lifespan=lifespan,
    title="Alpha API",
    version="1.0",
    description="🚀FastAPI backend application🚀",
)


origins = [
    "http://localhost",  # Дозволяє запити з localhost
    "http://localhost:3000",  # frontend
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api")
app.include_router(post_router, prefix="/api")
app.include_router(general_check_router, prefix="/api")
app.include_router(tag_router, prefix="/api")
app.include_router(images_router, prefix="/api")
app.include_router(comments_router, prefix="/api")
app.include_router(user_router, prefix="/api")
app.include_router(qr_code_router, prefix="/api")
app.include_router(admin_moderator_comments_router, prefix="/api")
app.include_router(admin_moderator_work_with_user_router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=base_config.start_app_config.APP_HOST, port=base_config.start_app_config.APP_PORT, reload=True)
