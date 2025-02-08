## Prueba Técnica - Desarrollador Backend Python

<p>Este repositorio contiene la solución a la prueba técnica propuesta por Verticcal para el puesto de desarrollador Backend. 
  El objetivo del proyecto es implementar tanto una API que consuma datos de una API externa como un sistema CRUD para gestionar información de leads utilizando Python, SQLAlchemy y PostgreSQL.
  La arquitectura sigue un diseño modular basado en capas (repositorio, servicio y modelo)
<p/>

### Tecnologias utilizadas

- Python
- FastAPI
- SQLAlchemy : ORM para interactuar con la base de datos.
- Psycopg2 : Adaptador PostgreSQL para Python.
- Pydantic : Para validación de datos
- PostgreSQL : Base de datos para almacenar Leads (Posibles clientes)
- Docker : Para creación de contenedores
  
Parte A
1. Consumo de una API pública
2. Creación de una API propia

¿Cómo ejecuto la API?

1. Crea un entorno virtual (python -m venv nombre_entorno_virtual)
2. Activa el entorno virtual (nombre_entorno_virtual/Scripts/activate para windows o source nombre_entorno_virtual/bin/activate para linux) 

Parte B
1.  Configurar PostgreSQL
2.  Script para procesar leads
3. Redacción de prompt para IA
