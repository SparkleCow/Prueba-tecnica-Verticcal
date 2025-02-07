import logging
import requests
from app.config.env import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_external_posts():
    try:
        response = requests.get("https://jsonplaceholder.typicode.com/posts", timeout=10) #TODO Implementar variable de entorno
        if response.status_code == 200:
            data = response.json()
            logger.info("Datos obtenidos exitosamente de la API externa.")
            return data
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