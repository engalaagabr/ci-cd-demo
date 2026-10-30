from fastapi import APIRouter
from app.api.endpoints.hello_world import router as hello_world_router

router = APIRouter()

router.include_router(hello_world_router, tags=["Hello World"])