from db.connection import DatabaseConnection
from repositories.lead_repository import LeadRepository
from services.lead_service import LeadService

# Configuración de la base de datos
DATABASE_URL = "postgresql://postgres:Borman15@localhost:5432/python"

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

<<<<<<< HEAD
=======
# Insertar leads
>>>>>>> 5ffde82552f75576d4888462c15f9e5fac94c7e7
session = db_connection.get_session()
repository = LeadRepository(session)
service = LeadService(repository)

<<<<<<< HEAD
# Insertar leads
try:
    repository.insert_leads(leads_data)
=======
try:
    repository.insert_leads(leads_data)
    print("Leads insertados exitosamente.")
>>>>>>> 5ffde82552f75576d4888462c15f9e5fac94c7e7
except ValueError as e:
    print(e)

# Procesar y presentar leads
results = service.process_and_present_leads(location="Medellín", min_budget=200000000, max_budget=600000000)
print(results)