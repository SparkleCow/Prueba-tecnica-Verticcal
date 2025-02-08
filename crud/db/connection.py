from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.lead import Base

class DatabaseConnection:
    
    """Clase para manejar la conexión a la base de datos"""
    
    def __init__(self, database_url: str):
        self.engine = create_engine(database_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def get_session(self):
        
        """Retorna una nueva sesión de base de datos"""
        
        return self.SessionLocal()
    
    def init_db(self):
        
        """Crea las tablas de acuerdo a las clases que heredan de Base"""

        Base.metadata.create_all(bind=self.engine)
