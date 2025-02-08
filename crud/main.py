from db.connection import DatabaseConnection
from repositories.lead_repository import LeadRepository
from services.lead_service import LeadService
from dotenv import load_dotenv
import os

# Configuración de la base de datos
DATABASE_URL = os.getenv("DATABASE_URL")
load_dotenv(dotenv_path="../.env") 
db_connection = DatabaseConnection(DATABASE_URL)

# Inicializar la base de datos
db_connection.init_db()

leads_data = [
    {"id": 1, "name": "Ana Salcedo", "location": "Medellín", "budget": 200000000},
    {"id": 2, "name": "Santiago Gallo", "location": "Medellín", "budget": 500000000},
    {"id": 3, "name": "Carlota Habib", "location": "Medellín", "budget": 650000000},
    {"id": 4, "name": "Pablo Sánchez", "location": "Bogotá", "budget": 350000000},
    {"id": 5, "name": "Andrés Arias", "location": "Bogotá", "budget": 150000000},
    {"id": 6, "name": "Andrés Limas", "location": "Bogotá", "budget": 450000000},
]

session = db_connection.get_session()
repository = LeadRepository(session)
lead_service = LeadService(repository)

# Insertar leads
try:
    repository.insert_leads(leads_data)
except ValueError as e:
    print(e)

print("Resultados filtrados por Budget \n")
results = lead_service.process_and_present_leads()
print(results)

print("Resultados filtrados por ciudad \n")
results = lead_service.process_and_present_leads(location="Medellín")
print(results)

# Insertar un nuevo lead
lead = {
            "name": "Santiago Moreno",
            "location": "Bogotá",
            "budget": 700000000
       }
#Insertamos un nuevo lead
lead_service.insert_lead(lead)

print("Resultados filtrados por Budget con el nuevo Lead \n")
results = lead_service.process_and_present_leads()
print(results)
