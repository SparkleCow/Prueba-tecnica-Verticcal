from pydantic import BaseModel

class Post(BaseModel):
    
    """Clase para representar los Posts provenientes de la API externa"""
    
    id: int
    userId: int
    title: str
    body: str
    
    class Config: 
        orm_mode = True
    