import psycopg2
from src.connectors.postgresqlcredenciales import postgresCredentials

connection = psycopg2.connect(
    host=postgresCredentials["host"],
    database=postgresCredentials["database"],
    user=postgresCredentials["user"],
    password=postgresCredentials["password"]
)
