from typing import Dict
from pydantic import BaseModel
from app.models.post import Post

class PostsStats(BaseModel):
    
    """Clase que representa las estadisticas de los Posts"""
    
    total_posts: int
    posts_per_user: Dict[int, int] 
    average_title_length: float
    average_body_length: float
    longest_post: Post
    shortest_post: Post