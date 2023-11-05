from app.api.routes.data import fixtures
from fastapi import FastAPI

from app.core.init_db import init_database_on_startup
from app.utils import get_logger

logger = get_logger("API Main App")


def get_application() -> FastAPI:
    application = FastAPI(
        title="Durhack2023",
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
