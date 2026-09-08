import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Procura o banco no caminho relativo local, na raiz do backend ou via variável de ambiente
candidatos_db = [
    os.getenv("DATABASE_PATH"),
    str(BASE_DIR.parent / "database" / "bimer.db"),
    str(BASE_DIR / "bimer.db"),
    str(BASE_DIR / "database" / "bimer.db"),
]

DATABASE_PATH = next((p for p in candidatos_db if p and Path(p).exists()), str(BASE_DIR.parent / "database" / "bimer.db"))
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
API_PREFIX = "/api/v1"
PROJECT_NAME = "Bimer Cloud - ERP Financeiro & Fiscal"
VERSION = "1.0.0"
TURSO_DATABASE_URL = os.getenv("TURSO_DATABASE_URL", "").strip()
TURSO_AUTH_TOKEN = os.getenv("TURSO_AUTH_TOKEN", "").strip()

