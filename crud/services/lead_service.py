from repositories.lead_repository import LeadRepository

class LeadService:
    
    """Servicio para procesar leads"""
    
    def __init__(self, repository: LeadRepository):
        self.repository = repository
        

    def process_and_present_leads(self, location=None, min_budget=None, max_budget=None):
        """Procesa los leads filtrando, calculando el presupuesto total y ordenando los resultados"""
        # Filtrar leads
        filtered_leads = self.repository.filter_leads(location, min_budget, max_budget)
        # Calcular el presupuesto total
        total_budget = sum(lead.budget for lead in filtered_leads)
        # Ordenar leads por presupuesto
        sorted_leads = sorted(filtered_leads, key=lambda lead: lead.budget, reverse=True)
        # Devolver los resultados
        return {
            "filtered_leads": [lead.to_dict() for lead in sorted_leads],
            "total_budget": total_budget
        }
    
    def insert_lead(self, lead_data: dict):
            """Inserta un nuevo lead en la base de datos."""
            try:
                self.repository.insert_lead(lead_data)
            except Exception as e:
                # Capturar y relanzar el error con un mensaje claro
                raise ValueError(f"Error al insertar el lead: {e}")