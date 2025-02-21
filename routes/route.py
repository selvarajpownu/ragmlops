from fastapi import APIRouter
from . import healthcheck, post_user_input

router = APIRouter()

healthcheck_handler = APIRouter()
healthcheck_handler.include_router(healthcheck.router)

postuserinput_handler = APIRouter()
postuserinput_handler.include_router(post_user_input.router)
