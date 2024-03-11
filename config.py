
# Importieren der benötigten Module
from dotenv import load_dotenv
import os

# Laden der Umgebungsvariablen aus einer .env-Datei
load_dotenv()

# Definition der Konfigurationsvariablen aus Umgebungsvariablen
SERVER_NAME = os.getenv("SERVER_NAME")
VERSION = os.getenv("VERSION")
PERSONAL_ACCESS_TOKEN_NAME = os.getenv("PERSONAL_ACCESS_TOKEN_NAME")
PERSONAL_ACCESS_TOKEN_SECRET = os.getenv("PERSONAL_ACCESS_TOKEN_SECRET")
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")
DB_SCHEMA = os.getenv("DB_SCHEMA")