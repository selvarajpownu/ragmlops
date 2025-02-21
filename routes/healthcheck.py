from fastapi import APIRouter
from http import HTTPStatus

router = APIRouter()

@router.get("/healthcheck")
async def health_check() -> dict:
    return {
        'Status': HTTPStatus.OK,
        'Message': "Health check test passed"
    }