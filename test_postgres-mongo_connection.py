import os
import psycopg2
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def connect_to_postgres():
    try:
        conn = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT"),
            database=os.getenv("POSTGRES_DATABASE"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD")
        )
        print("Conexión exitosa a PostgreSQL.")
        return conn
    except psycopg2.Error as e:
        print("Error al conectar a PostgreSQL:", e)
        return None

def connect_to_mongodb():
    try:
        client = MongoClient(os.getenv("MONGODB_URI"))
        db = client[os.getenv("MONGODB_DATABASE")]
        collection_names = db.list_collection_names()
        if collection_names:
            print("Conexión exitosa a MongoDB.")
        else:
            print("No hay colecciones en la base de datos MongoDB.")
        client.close()
    except Exception as e:
        print("Error al conectar a MongoDB:", e)

if __name__ == "__main__":
    postgres_conn = connect_to_postgres()
    if postgres_conn:
        postgres_conn.close()
        connect_to_mongodb()
    else:
        print("No se pudo establecer la conexión a PostgreSQL.")
