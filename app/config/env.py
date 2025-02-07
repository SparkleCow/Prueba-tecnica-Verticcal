from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv("../../.env")

class Settings(BaseModel):
    database_url: str = os.getenv("DATABASE_URL")
    external_api_url: str = os.getenv("EXTERNAL_API_URL")

settings = Settings()
