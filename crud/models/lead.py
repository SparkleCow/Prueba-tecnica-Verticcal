from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Lead(Base):
    
    """Modelo que representa la tabla leads en la base de datos"""
    
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    location = Column(String, index=True)
    budget = Column(Float)

    def to_dict(self):
        
        """Convierte el objeto Lead a un diccionario"""
        
        return {
            "id": self.id,
            "name": self.name,
            "location": self.location,
            "budget": self.budget
        }