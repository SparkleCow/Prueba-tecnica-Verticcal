from sqlalchemy.orm import Session
from models.lead import Lead

class LeadRepository:
    
    """Repositorio para interactuar con los leads en la base de datos"""
    
    def __init__(self, session: Session):
        self.session = session

    def insert_leads(self, leads_data):
        
        """Inserta una lista de leads en la base de datos solo si no existen previamente"""
        
        try:
            for lead in leads_data:
                # Verificamos si el lead ya existe
                existing_lead = self.session.query(Lead).filter_by(id=lead["id"])
                if not existing_lead:
                    db_lead = Lead(**lead)
                    self.session.add(db_lead)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise ValueError(f"Error al insertar leads: {e}")

    def filter_leads(self, location=None, min_budget=None, max_budget=None):
        
        """Filtra los leads por ubicación y/o rango de presupuesto"""
        
        query = self.session.query(Lead)
        if location:
            query = query.filter(Lead.location == location)
        if min_budget is not None:
            query = query.filter(Lead.budget >= min_budget)
        if max_budget is not None:
            query = query.filter(Lead.budget <= max_budget)
        return query.all()

    