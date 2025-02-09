# Prueba Técnica - Desarrollador Backend Python

<p>Este repositorio contiene la solución a la prueba técnica propuesta por Verticcal para el puesto de desarrollador Backend. 
  El objetivo del proyecto es implementar tanto una API que consuma datos de una API externa como un sistema CRUD para gestionar información de leads utilizando Python, SQLAlchemy y PostgreSQL.
  La arquitectura sigue un diseño modular basado en capas (repositorio, servicio y modelo)
<p/>

## Tecnologias utilizadas

- Python y FastAPI
- SQLAlchemy y Psycopg2
- Pydantic
- PostgreSQL 
- Docker
- Postman

## Instalación: 

1. Descarga el proyecto: Clona el repositorio con git clone https://github.com/SparkleCow/Prueba-tecnica-Verticcal.git o descarga el repositorio en formato .rar para poder manipularlo.
2. Crea un entorno virtual (python -m venv nombre_entorno_virtual)
3. Activa el entorno virtual (nombre_entorno_virtual/Scripts/activate para windows o source nombre_entorno_virtual/bin/activate para linux)
4. Instalar las dependencias del proyecto (pip install -r requirements.txt)
5. Crea el archivo .env para las variables de entorno (DATABASE_URL, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB, POSTGRES_PORT)
7. Crea un contenedor con docker por medio del archivo docker-compose.yml para ejecutar postgres (docker-compose up -d). El archivo docker-compose.yml hace uso del archivo .env
8. En caso de usar postgres a nivel local, modificar el archivo .env con las credenciales.
9. Para arrancar el servidor de fastAPI sera necesario emplear Uvicorn (uvicorn app.main:app --reload)
10. Para ver los endpoints disponibles entrar a http://localhost:8000/docs
11. Para hacer peticiones a la API, utiliza la ruta base http://localhost:8000/api/v1/external-data
  
## Parte A

1. Consumo de una API pública
2. Creación de una API propia

## API

La API realizada consume información de JSONPlaceHolder, especificamente de la entidad Post. 
Por su parte, también modifica y crea estadísticas a partir de los datos recibidos.

### Modelos

#### `PostsStats`

Clase que representa las estadísticas de los Posts.

```python
from typing import Dict
from pydantic import BaseModel
from app.models.post import Post

class PostsStats(BaseModel):
    """Clase que representa las estadisticas de los Posts"""
    total_posts: int
    posts_per_user: Dict[int, int] 
    average_title_length: float
    average_body_length: float
    longest_post: Post
    shortest_post: Post
```
#### `Posts` 

Clase para representar y validad los Posts provenientes de la API externa y validar los datos enviados desde la API realizada
<br>

```python
from pydantic import BaseModel

class Post(BaseModel):
    """Clase para representar los Posts provenientes de la API externa"""
    id: int
    userId: int
    title: str
    body: str
    
    class Config: 
        orm_mode = True
```
### Ejemplos de uso de los endpoints de la API

1. Obtener Estadísticas de Posts

  - Método : GET
  - Ruta : /api/v1/external-data/stats
  - Descripción : Calcula estadísticas generales sobre los posts, como el número total de posts, promedio de longitud de títulos y cuerpos, y retorna el posts más largo y el más corto.

  ![image](https://github.com/user-attachments/assets/9861d011-27a0-4855-8ea0-57b4e8739536)

2. Obtener Todos los Posts
   
  - Método : GET
  - Ruta : /api/v1/external-data
  - Descripción : Devuelve una lista de todos los posts disponibles.

  ![image](https://github.com/user-attachments/assets/2da561d2-dee8-4967-9b55-347abf6ea52b)

3. Filtrar los Post según una palabra clave
   
  - Método : GET
  - Ruta : /api/v1/external-data/search?query=value
  - Descripción : Devuelve una lista de todos los posts que contengan en el título la palabra enviada en la query

  ![image](https://github.com/user-attachments/assets/64b11b64-74f9-4168-84bc-b53e76060b1c)

    
Parte B
1.  Configurar PostgreSQL
2.  Script para procesar leads
3. Redacción de prompt para IA

## Servicio de manipulación de datos

El servicio implementado permite realizar operaciones básicas de gestión de datos sobre una base de datos de leads. 

### Modelo ORM

Se empleó un modelo ORM por medio de slqalchemy para validar la información enviada y recibida de la base de datos. 

#### Lead 

Clase para validar y representar y la tabla leads en la base de datos. 
<br>

```python
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Lead(Base):
    """Modelo que representa la tabla leads en la base de datos"""
    __tablename__ = "leads"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
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
```
A continuación, se describen los resultados obtenidos al ejecutar las principales funcionalidades del sistema.

1. Insertar leads por medio de un diccionario:

  Este codigo permite ingresar el diccionario e introducirlos a la base de datos almacenandolos como objetos Lead.

  ```python
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
  ```
2. Insertar un nuevo lead:

  Por medio de este código, se recibe un diccionario con la información del nuevo Lead sin introducir el id. 
  Este lead se incorporara en la base de datos con un nuevo id (Auto incremental)


  ```python
    def insert_lead(self, lead: dict):
        """Inserta un nuevo Lead en la base de datos"""
        try:
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
  ```

3. Filtrar leads:

  El servicio permite filtrar leads de acuerdo a tres parametos; localización, un mínimo de presupuesto o un máximo de presupuesto.

  ```python

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
  ```

4. Calcular presupuesto total:

  Se calcula el presupuesto total de acuerdo a la cantidad de los leads ingresados

  ```python

      def calculate_total_budget(self) -> float:
              """Calcula el presupuesto total de los leads proporcionados"""
              all_leads = self.session.query(Lead).all()
              total_budget = 0.0
              for lead in all_leads:
                  total_budget += lead.budget
              return total_budget
  ```

5. Organizar leads de acuerdo a su presupuesto:

  Se organizan los leads según su presupuesto y devuelve la lista de mayor a menor o de menor a mayor segun el valor booleanos ingresado como argumento
  
  ```python

    def sort_leads_by_budget(self, descending: bool = True) -> List[Lead]:
        """Ordena los leads por presupuesto"""
        all_leads = self.session.query(Lead).all()
        if descending:
            all_leads.sort(key=lambda lead: lead.budget, reverse=True) 
        else:
            all_leads.sort(key=lambda lead: lead.budget)
        return all_leads
  ```

### Presentación de los datos

Al ejecutar el modulo principal el código de cada uno de los servicios anteriormente mencionados dando como resultado la siguiente respuesta en consola:

![image](https://github.com/user-attachments/assets/2530711d-deb2-4d5b-b2b2-ef2cf3c0134d)


## Prompt para IA 

Quiero que generes un correo electrónico personalizado y profesional dirigido a un posible cliente (lead). Un lead es una persona que ha mostrado interés en nuestros servicios o productos inmobiliarios y está considerando trabajar con nosotros. Somos una empresa especializada en la venta de inmuebles de alta calidad, y nuestro equipo tiene amplia experiencia ayudando a clientes a encontrar propiedades que se ajusten a sus necesidades y presupuesto.

Usa los siguientes datos del lead para personalizar el mensaje:

Nombre del lead : Jonathan David Ramos
Ubicación del lead : Bogotá
Presupuesto del lead : 120,000,000
El correo debe incluir los siguientes elementos:

Usa el nombre del lead para hacerlo sentir valorado.
Expresa interés genuino en ayudar al lead con sus necesidades específicas de compra de inmuebles. Menciona que somos expertos en el mercado inmobiliario y que entendemos las particularidades de cada zona y/o región.
Haz referencia a su ciudad o región para demostrar que estamos atentos a su contexto local y conocemos el mercado inmobiliario de esa área.
Indica que ofrecemos propiedades que se ajustan perfectamente a su rango de inversión, basándonos en el presupuesto proporcionado.
Invita al lead a programar una reunión o visita guiada para explorar opciones de inmuebles disponibles. También ofrece proporcionar más información sobre las propiedades que podrían interesarle.
Incluye una firma profesional con tu nombre, cargo, empresa y datos de contacto.
El tono debe ser amigable pero formal, adecuado para una comunicación empresarial en el sector inmobiliario. Asegúrate de que el correo sea conciso, profesional y fácil de leer. 
Además, destaca nuestra experiencia en el mercado inmobiliario para generar confianza en el lead.

## Respuesta de ChatGPT

Asunto: Jonathan, tenemos la propiedad ideal para ti en Bogotá

Estimado Jonathan David Ramos,

Espero que este mensaje te encuentre bien. Me comunico contigo en nombre de Amarilo, una empresa con amplia experiencia en el mercado inmobiliario, comprometida en ayudar a clientes como tú a encontrar la propiedad ideal según sus necesidades y presupuesto.

Sabemos que estás interesado en adquirir una propiedad en Bogotá y que cuentas con un presupuesto de $120,000,000. Nos especializamos en ofrecer inmuebles de alta calidad y queremos ayudarte a encontrar la mejor opción dentro de tu rango de inversión. Conocemos a profundidad el mercado inmobiliario de la ciudad y podemos asesorarte para que tomes la mejor decisión.

Nos encantaría agendar una reunión o visita guiada para mostrarte algunas opciones que se ajustan a tus expectativas. También podemos enviarte información detallada sobre propiedades que pueden ser de tu interés.

Por favor, dime cuándo estarías disponible para coordinar una reunión o visita. Estaremos encantados de acompañarte en cada paso del proceso para que encuentres el hogar perfecto.

Quedo atento a tu respuesta.

Saludos cordiales,

- [Tu Nombre] Asesor Inmobiliario
- [Tu correo electrónico]
- [Tu número de teléfono]
- [www.amarilo.com]
