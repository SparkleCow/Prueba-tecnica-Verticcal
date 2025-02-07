from fastapi import APIRouter, HTTPException

external_data_router = APIRouter(prefix="/api/v1")

@external_data_router.get("/external_data", status_code=200)
def list_posts():
    pass