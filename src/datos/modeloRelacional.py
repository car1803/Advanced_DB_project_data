from src.connectors.connection import connection

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
        CREATE SCHEMA IF NOT EXISTS {schema} AUTHORIZATION cloudsqlsuperuser;
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

def create_tables(migration_file):
    import os

    print("Creando tablas con el archivo de migración...", migration_file)
    ruta_script = os.path.abspath(__file__)  # Ruta absoluta del script actual
    directorio_script = os.path.dirname(ruta_script) 
    print(directorio_script)
    ruta_archivo = directorio_script + f'\\migrations\\{migration_file}.sql'
    print(ruta_archivo)
        # Leer el contenido del archivo
    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        contenido = archivo.read()
        cursor = connection.cursor()
        print("Creando tablas...")
        cursor.execute(contenido)

    print("Tablas creadas.")
    connection.commit()

if __name__ == '__main__':
    create_tables()