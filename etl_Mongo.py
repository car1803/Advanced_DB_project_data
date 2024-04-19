import os
import psycopg2
from dotenv import load_dotenv
from pymongo import MongoClient

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
        return conn
    except psycopg2.Error as e:
        print("Error al conectar a PostgreSQL:", e)
        return None

def fetch_dimensional_data(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                he.id, t.*, e.*, em.*, tec.*, c.*, hec.*, s.*, te.*, hei.*, i.*, idn.*, ec.*
            FROM htrabajoestudiante he
            JOIN dtiempo t ON he."fechainicioid" = t.id
            JOIN destudiante e ON he."estudianteid" = e.id
            JOIN dempresa em ON he."empresaid" = em.id
            LEFT JOIN dtrabajoestudiantecarrera tec ON he.id = tec."trabajoestudianteid"
            LEFT JOIN dcarrera c ON tec."carreraid" = c.id
            LEFT JOIN hempresa hec ON he."empresaid" = hec.id
            LEFT JOIN dsector s ON hec."sectorid" = s.id
            LEFT JOIN dtipoempresa te ON hec."tipoempresaid" = te.id
            LEFT JOIN hestudianteidioma hei ON he."estudianteid" = hei."estudianteid"
            LEFT JOIN didioma i ON hei."idiomaid" = i.id
            LEFT JOIN didiomanivel idn ON hei."idiomanivelid" = idn.id
            LEFT JOIN dempresacarrera ec ON em.id = ec."empresaid"
            LEFT JOIN destudianteidiomaempresa eie ON em.id = eie."empresaid"
            LEFT JOIN destudianteidiomacarrera eic ON c.id = eic."carreraid"
        """)
        return cursor.fetchall()
    except psycopg2.Error as e:
        print("Error al recuperar los datos dimensionales:", e)
        return None

def load_to_mongodb(data, fact_table_name):
    try:
        client = MongoClient(os.getenv("MONGODB_URI"))
        db = client[os.getenv("MONGODB_DATABASE")]
        for row in data:
            document = {}
            # Agregar datos de dTiempo
            document['tiempo'] = {
                'fechaInicio': row[1],
                'year': row[2],
                'month': row[3],
                'day': row[4]
            }
            
            # Agregar datos de dEstudiante
            document['estudiante'] = {
                'nombre': row[5],
                'correo': row[6],
                'apellido': row[7],
                'fechaNacimiento': row[8],
                'genero': row[9],
                'documento': row[10],
                'nombrePais': row[11],
                'nombreTipoDocumento': row[12]
            }
            
            # Agregar datos de dEmpresa
            document['empresa'] = {
                'nombre': row[13],
                'correo': row[14],
                'web': row[15],
                'nombreSector': row[16],
                'nombreTipo': row[17]
            }
            
            # Agregar datos de dCarrera
            document['carrera'] = {
                'nombre': row[18],
                'nombreTipoCarrera': row[19],
                'nombreDepartamento': row[20],
                'nombreFacultad': row[21],
                'nombreSede': row[22]
            }
            
            # Agregar datos de hTrabajoEstudiante
            document['trabajoEstudiante'] = {
                'fechaFinId': row[23],
                'orden': row[24],
                'cargo': row[25],
                'añosExperienciaPrevia': row[26],
                'salarioPromedio': row[27],
                'ofertaSie': row[28]
            }
            
            # Agregar datos de dSector
            document['sector'] = {
                'nombre': row[30]
            }
            
            # Agregar datos de dTipoEmpresa
            document['tipoEmpresa'] = {
                'nombre': row[31]
            }
            
            # Agregar datos de hEmpresa
            document['empresa_h'] = {
                'correo': row[32],
                'web': row[33],
                'gastoEnSalariosTotal': row[34],
                'numeroDeEmpleadosTotal': row[35],
                'numerodeEmpleadosActual': row[36]
            }
            
            # Agregar datos de dEmpresaCarrera
            document['empresa_carrera'] = {
                'carreraId': row[37]
            }
            
            # Agregar datos de dIdioma
            document['idioma'] = {
                'nombre': row[38]
            }
            
            # Agregar datos de dIdiomaNivel
            document['idiomaNivel'] = {
                'nombre': row[39]
            }
            
            # Insertar el documento en la colección MongoDB correspondiente
            db[fact_table_name].insert_one(document)

        print("Datos insertados en MongoDB correctamente.")
    except Exception as e:
        print("Error al cargar datos en MongoDB:", e)

if __name__ == "__main__":
    postgres_conn = connect_to_postgres()
    if postgres_conn:
        print("Conexión exitosa a PostgreSQL.")
        dimensional_data = fetch_dimensional_data(postgres_conn)
        if dimensional_data:
            fact_table_name = "egresado"
            load_to_mongodb(dimensional_data, fact_table_name)
        else:
            print("No se pudieron recuperar los datos dimensionales.")
        postgres_conn.close()
    else:
        print("No se pudo establecer la conexión a PostgreSQL.")



