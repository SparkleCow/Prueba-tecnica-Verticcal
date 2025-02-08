from typing import List
from fastapi import APIRouter, HTTPException, Query
from app.models.post import Post
from app.services.external_api import get_external_posts
from app.services.post_service import generate_stats, search_posts


router = APIRouter(prefix="/api/v1")


@router.get("/external-data", response_model=List[Post], status_code=200)
def get_posts():
    """ Obtiene todos los posts desde la API externa o el cache"""
    try:
        posts = get_external_posts()
        if not posts:
            raise HTTPException(status_code=500, detail="No se pudieron obtener los datos de la API externa")
        return posts
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    
    
@router.get("/external-data/stats", status_code=200)
def get_posts_stats():
    """Genera estadisticas sobre los posts obtenidos de la API externa."""
    try:
        posts = get_external_posts()
        if not posts:
            raise HTTPException(status_code=500, detail="No se pudieron obtener los datos de la API externa")
        return generate_stats(posts)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar las estadisticas: {str(e)}")
    
    
@router.get("/external-data/search", status_code=200)
async def search_posts_endpoint(query: str = Query(..., min_length=1, description="Palabra para buscar en los posts")):
    """Busca posts que contengan una palabra clave en el titulo o cuerpo."""
    try:
        posts = get_external_posts()
        if not posts:
            raise HTTPException(status_code=500, detail="No se pudieron obtener los datos de la API externa")
        
        results = search_posts(posts, query)
        if not results:
            raise HTTPException(status_code=404, detail=f"No se encontraron posts con el titulo que coincidan con la palabra clave: {str(query)}")
        
        return results
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=f"Parametro de busqueda invalido: {str(ve)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al realizar la busqueda: {str(e)}")