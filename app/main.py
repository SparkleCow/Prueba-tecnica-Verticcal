from fastapi import FastAPI
from app.routes.posts_route import router
from app.routes.external_data_route import external_data_router


app = FastAPI()
app.include_router(router)
app.include_router(external_data_router)