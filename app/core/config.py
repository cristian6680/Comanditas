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

    # Configuración de seguridad JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "CLAVE_SECRETA_SUPER_CONFIDENCIAL_QUILMES_2026_COMANDITAS")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # El token dura 24 horas
    
settings = Settings()
