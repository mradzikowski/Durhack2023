from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def retrieval_of_data_with_link():
    return {"status": "ok"}