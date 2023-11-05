import os

from app.api.routes.data import fixtures
from app.core.init_db import init_database_on_startup
from app.machine_learning_models.predictorr import training_the_model
from app.utils import get_logger
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

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

    if os.path.exists("predicting_ftag.pkl") and os.path.exists("predicting_fthg.pkl"):
        logger.info("Models already trained")
    else:
        await training_the_model()


@app.on_event("shutdown")
async def shutdown_event():
    """
    Event on shutdown
    """
    logger.info("Shutting down...")
