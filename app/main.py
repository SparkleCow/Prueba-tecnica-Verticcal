from fastapi import FastAPI
from app.routes.posts_route import router

app = FastAPI()
app.include_router(router)
