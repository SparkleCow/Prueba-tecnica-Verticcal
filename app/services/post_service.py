from typing import List
from app.models.post import Post
from app.models.post_stats import PostsStats


def generate_stats(posts: List[Post]) -> PostsStats:
    
    """Genera estadísticas sobre los posts"""
    
    total_posts = len(posts)
    posts_per_user = {}
    total_title_length = 0
    total_body_length = 0
    longest_post = None
    shortest_post = None

    for post in posts:
        user_id = post.userId
        title_length = len(post.title)
        body_length = len(post.body)

        # Contamos los posts por usuario
        posts_per_user[user_id] = posts_per_user.get(user_id, 0) + 1
        # Acumular longitudes para sacar los promedios 
        total_title_length += title_length
        total_body_length += body_length

        # Identificar el post más largo y el más corto
        if longest_post is None or body_length > len(longest_post.body):
            longest_post = post
        if shortest_post is None or body_length < len(shortest_post.body):
            shortest_post = post

    average_title_length = total_title_length / total_posts if total_posts > 0 else 0
    average_body_length = total_body_length / total_posts if total_posts > 0 else 0

    return PostsStats(
        total_posts=total_posts,
        posts_per_user=posts_per_user,
        average_title_length=round(average_title_length, 2),
        average_body_length=round(average_body_length, 2),
        longest_post=longest_post,
        shortest_post=shortest_post
    )
    
    
def search_posts(posts: List[Post], query: str) -> List[Post]:
    
    """Busca posts que contengan una palabra clave en el título"""
    
    query = query.lower()
    result = []
    
    for post in posts:
        if query in post.title.lower():
            result.append(post)
    
    return result