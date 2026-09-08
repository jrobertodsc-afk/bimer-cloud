import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DEFAULT_DB_PATH = BASE_DIR.parent / "database" / "bimer.db"

DATABASE_PATH = os.getenv("DATABASE_PATH", str(DEFAULT_DB_PATH))
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
API_PREFIX = "/api/v1"
PROJECT_NAME = "Bimer Cloud - ERP Financeiro & Fiscal"
VERSION = "1.0.0"
