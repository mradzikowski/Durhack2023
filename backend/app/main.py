from starlette.middleware.cors import CORSMiddleware

from app.api.routes.data import fixtures
from fastapi import FastAPI

from app.core.init_db import init_database_on_startup
from app.utils import get_logger

logger = get_logger("API Main App")


def get_application() -> FastAPI:
    application = FastAPI(
        title="Durhack2023",
    )

    origins = [
        "http://localhost:3000",
        "https://localhost:3000",
    ]
    # application.add_middleware(HTTPSRedirectMiddleware)
    # ADDED ALLOWED HEADERS AS IN TUTORIAL
    allowed_headers = [
        "date",
        "transfer-encoding",
        "accept",
        "accept-encoding",
        "host",
        "origin",
        "referer",
        "user-agent",
        "content-encoding",
        "content-length",
        "content-type",
        "cookie",
    ]
    application.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_methods=["*"],
        allow_headers=allowed_headers,
        allow_credentials=True,
    )

    application.include_router(
        fixtures.router,
        prefix="/fixtures",
        tags=["fixtures"],
    )

    return application


app = get_application()


@app.on_event("startup")
async def startup_event():
    """
    Event on startup to start the database
    """
    logger.info("Starting up...")
    await init_database_on_startup()


@app.on_event("shutdown")
async def shutdown_event():
    """
    Event on shutdown
    """
    logger.info("Shutting down...")
