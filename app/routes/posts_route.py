from fastapi import APIRouter, HTTPException
from app.services.external_api import get_external_posts
from app.services.post_service import generate_stats, search_posts

router = APIRouter(prefix="/api/v1")

@router.get("/external-data", status_code=200)
def get_posts():
    try:
        return get_external_posts()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    
@router.get("/external-data/stats")
def get_posts_stats():
    try:
        return generate_stats(get_external_posts())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
@router.get("/external-data/search")
async def search_posts_endpoint(query: str):
    try:
        return search_posts(get_external_posts(), query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al realizar la búsqueda: {str(e)}")