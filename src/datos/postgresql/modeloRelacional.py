from src.connectors.postgresql.connection import connection
import os

def drop_schema(schema):
    cursor = connection.cursor()

    print("Eliminando esquema "+schema+"...")

    cursor.execute(f'''
        DROP SCHEMA IF EXISTS {schema} CASCADE;
    ''')

    print("Esquema eliminado.")
    connection.commit()

def create_schema(schema):
    cursor = connection.cursor()

    print("Creando esquema esquema "+schema+"...")

    cursor.execute(f'''
        CREATE SCHEMA IF NOT EXISTS {schema};
    ''')

    print("Esquema creado.")
    connection.commit()

def set_schema(schema):
    cursor = connection.cursor()

    print("Estableciendo esquema "+schema+"...")

    cursor.execute(f'''
        SET search_path TO {schema};
    ''')

    print("Esquema establecido.")
    connection.commit()

def execute_script(migration_file):
    print("Ejecutando Script con el archivo de migración...", migration_file)
    directorio_script = os.path.dirname(os.path.abspath(__file__))
    directorio_migraciones = os.path.join(directorio_script, "..", "migrations")
    ruta_archivo = os.path.join(directorio_migraciones, f"{migration_file}.sql")
    print("Ruta del archivo:", ruta_archivo)
    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        contenido = archivo.read()
        cursor = connection.cursor()
        print("Ejecutando script...")
        cursor.execute(contenido)

    print("Proceso Finalizado.")
    connection.commit()

def execute_script_by_steps(migration_file):
    print("Ejecutando Script por pasos con el archivo de migración...", migration_file)
    directorio_script = os.path.dirname(os.path.abspath(__file__))
    directorio_migraciones = os.path.join(directorio_script, "..", "migrations")
    ruta_archivo = os.path.join(directorio_migraciones, f"{migration_file}.sql")
    print("Ruta del archivo:", ruta_archivo)
    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        contenido = archivo.read()
        queries = contenido.split(';')
        cursor = connection.cursor()
        for query in queries:
            query = query.strip()
            if not query:
                continue 
            print("Ejecutando script...")
            print(query)
            cursor.execute(query)
            connection.commit()
            print("Hecho...")
    print("Proceso Finalizado.")
    connection.commit()