from fastapi import FastAPI
from api.routes.data import retrieval

def get_application() -> FastAPI:
    application = FastAPI(
        title="Durhack2023",
    )

    application.include_router(
        retrieval.router,
        prefix="/data",
        tags=["data"],
    )

    return application

app = get_application()


@app.on_event("startup")
async def startup_event():
    """
    Event on startup to start the database
    """
    logger.info("Starting up...")


@app.on_event("shutdown")
async def shutdown_event():
    """
    Event on shutdown
    """
    logger.info("Shutting down...")