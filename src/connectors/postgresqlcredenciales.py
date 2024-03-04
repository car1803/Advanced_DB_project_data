from dotenv import load_dotenv
import os

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Acceder a las variables de entorno cargadas
postgresCredentials = {
    "host": os.getenv("POSTGRES_HOST"),
    "database": os.getenv("POSTGRES_DATABASE"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD")
}

postgresUri = f"postgresql://{postgresCredentials['user']}:{postgresCredentials['password']}@{postgresCredentials['host']}/{postgresCredentials['database']}"