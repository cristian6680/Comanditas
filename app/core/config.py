import os
from dotenv import load_dotenv
load_dotenv()
class Settings:
    PROYECT_NAME: str = "Comanditas API"
    VERSION: str = "1.0.0"
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://comanditas_user:comanditas123@localhost:5432/comanditas_db"
    )

settings = Settings()
