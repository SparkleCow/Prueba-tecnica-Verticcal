import logging
import requests
import time
from typing import List, Optional
from app.models.post import Post

# Configuración del logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Variables globales para almacenar los posts en cache
posts: Optional[List[Post]] = None
last_request_time = 0
current_time = 0
time_caching = 300 

def get_external_posts() -> List[Post]:
    
    global posts, last_request_time
    current_time = time.time()
    
    #Si los datos estan en cache y el tiempo de la ultima petición es menor a 5 minutos, devolvemos la lista con la información
    if posts and (current_time-last_request_time < time_caching):
        last_request_time = time.time()
        return posts
    
    #Si no hay nada en cache, hacemos una petición a la API y actualizamos la variable con la información del momento de la ultima petición (last_request_time)
    try:
        response = requests.get("https://jsonplaceholder.typicode.com/posts", timeout=10) #TODO Implementar variable de entorno
        if response.status_code == 200:
            data = response.json()
            posts = [Post(**post) for post in data]
            last_request_time = time.time()
            logger.info("Datos obtenidos exitosamente de la API externa.")
            return posts
        else:
            logger.error(f"Error al consumir la API externa. Código de estado: {response.status_code}")
            return None
    except requests.exceptions.Timeout:
        logger.error("La solicitud a la API externa ha excedido el tiempo de espera.")
    except requests.exceptions.ConnectionError:
        logger.error("Error de conexión al intentar acceder a la API externa.")
    except Exception as e:
        logger.error(f"Error inesperado al consumir la API externa: {e}")
        return None