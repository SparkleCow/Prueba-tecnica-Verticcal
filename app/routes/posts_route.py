from fastapi import APIRouter, HTTPException
from app.services.external_api import get_external_posts

router = APIRouter(prefix="/api/v1")

@router.get("/post", status_code=200)
def list_posts():
    try:
        return get_external_posts()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))