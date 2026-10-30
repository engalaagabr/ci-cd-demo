from fastapi import FastAPI
from app.api.routers.hello_world import router as hello_world_router


app = FastAPI()

app.include_router(hello_world_router)
