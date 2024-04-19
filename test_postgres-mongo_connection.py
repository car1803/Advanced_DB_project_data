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
        print("Conexión exitosa a MongoDB.")
        # # Insertar datos en la colección de MongoDB
        # collection = db["nombre_de_la_coleccion"]  # Reemplaza "nombre_de_la_coleccion" por el nombre de tu colección
        # # Supongamos que tienes datos en forma de diccionarios llamados data_list
        # data_list = [{"campo1": "valor1"}, {"campo2": "valor2"}]  # Ejemplo de datos a insertar
        # collection.insert_many(data_list)
        # print("Datos insertados en la colección de MongoDB.")
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
