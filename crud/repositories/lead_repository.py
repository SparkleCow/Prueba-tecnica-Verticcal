from typing import List
from sqlalchemy import func
from sqlalchemy.orm import Session
from models.lead import Lead

class LeadRepository:
    
    """Repositorio para interactuar con los leads en la base de datos"""
    
    
    def __init__(self, session: Session):
        self.session = session
        

    def insert_leads(self, leads_data: List[dict]):
        """Inserta una lista de Leads en la base de datos solo si no existen previamente"""
        try:
            for lead in leads_data:
                # Verificamos si los leads ya existen
                existing_lead = self.session.query(Lead).filter_by(id=lead["id"]).first()
                if not existing_lead:
                    db_lead = Lead(**lead)
                    self.session.add(db_lead)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise ValueError(f"Error al insertar leads: {e}")
        
        
    def insert_lead(self, lead: dict):
        """Inserta un nuevo Lead en la base de datos"""
        try:
            # Obtener el último ID existente en la tabla
            last_id = self.session.query(func.max(Lead.id)).scalar() or 0
            # Asignar manualmente el siguiente ID
            next_id = last_id + 1
            lead["id"] = next_id
            new_lead = Lead(**lead)
            self.session.add(new_lead)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise ValueError(f"Error al insertar el lead: {e}")


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
    
    
    def calculate_total_budget(self) -> float:
        """Calcula el presupuesto total de los leads proporcionados"""
        all_leads = self.session.query(Lead).all()
        total_budget = 0.0
        for lead in all_leads:
            total_budget += lead.budget
        return total_budget
    
    
    def sort_leads_by_budget(self, descending: bool = True) -> List[Lead]:
        """Ordena los leads por presupuesto"""
        all_leads = self.session.query(Lead).all()
        if descending:
            all_leads.sort(key=lambda lead: lead.budget, reverse=True) 
        else:
            all_leads.sort(key=lambda lead: lead.budget)
        return all_leads