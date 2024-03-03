from src.connectors.connection import connection

def drop_schema(schema="testmodel"):
    cursor = connection.cursor()

    print("Eliminando esquema testmodel...")

    cursor.execute(f'''
        DROP SCHEMA IF EXISTS {schema} CASCADE;
    ''')

    print("Esquema eliminado.")
    connection.commit()

def create_schema(schema="testmodel"):
    cursor = connection.cursor()

    print("Creando esquema testmodel...")

    cursor.execute(f'''
        CREATE SCHEMA IF NOT EXISTS {schema} AUTHORIZATION cloudsqlsuperuser;
    ''')

    print("Esquema creado.")
    connection.commit()

def create_tables(schema="testmodel"):
    cursor = connection.cursor()
    
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {schema}.pais (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(255) NOT NULL
        )
    ''')
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {schema}.tipoDocumento (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(255) NOT NULL
        )
    ''')
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {schema}.estudiante (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(255) NOT NULL,
            correo VARCHAR(255) NOT NULL,
            apellido VARCHAR(255) NOT NULL,
            fechaNacimiento DATE NOT NULL,
            genero VARCHAR(1) NOT NULL,
            documento VARCHAR(255) NOT NULL,
            paisId INT NOT NULL, 
            tipoDocumentoId INT NOT NULL, 
            FOREIGN KEY (paisId) REFERENCES {schema}.pais (id), 
            FOREIGN KEY (tipoDocumentoId) REFERENCES {schema}.tipoDocumento (id)
        )
    ''')
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {schema}.tipoCarrera (
            id SERIAL PRIMARY KEY, 
            nombre VARCHAR(255) NOT NULL
        )
    ''')
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {schema}.sede (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(255) NOT NULL
        )
    ''')
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {schema}.facultad (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(255) NOT NULL,
            sedeId INTEGER NOT NULL,
            FOREIGN KEY (sedeId) REFERENCES {schema}.sede(id)
        )
    ''')
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {schema}.departamento (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(255) NOT NULL,
            facultadId INTEGER NOT NULL,
            FOREIGN KEY (facultadId) REFERENCES {schema}.facultad(id)
        )
    ''')
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {schema}.carrera (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(255) NOT NULL,
            tipoCarreraId INTEGER NOT NULL,
            departamentoId INTEGER NOT NULL,
            FOREIGN KEY (tipoCarreraId) REFERENCES {schema}.tipoCarrera(id),
            FOREIGN KEY (departamentoId) REFERENCES {schema}.departamento(id)
        )
    ''')
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {schema}.egresado (
            id SERIAL PRIMARY KEY,
            año INT NOT NULL,
            carreraId INT NOT NULL,
            estudianteId INT NOT NULL,
            FOREIGN KEY (carreraId) REFERENCES {schema}.carrera (id),
            FOREIGN KEY (estudianteId) REFERENCES {schema}.estudiante (id)
        )
    ''')
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {schema}.idioma (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(255) NOT NULL
        )
    ''')
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {schema}.idiomaNivel (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(255) NOT NULL
        )
    ''')
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {schema}.estudianteIdioma (
            id SERIAL PRIMARY KEY,
            idiomaId INTEGER NOT NULL,
            idiomaNivelId INTEGER NOT NULL,
            estudianteId INTEGER NOT NULL,
            FOREIGN KEY (idiomaId) REFERENCES {schema}.idioma(id),
            FOREIGN KEY (idiomaNivelId) REFERENCES {schema}.idiomaNivel(id),
            FOREIGN KEY (estudianteId) REFERENCES {schema}.estudiante(id)
        )
    ''')
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {schema}.institucionExterna (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(255) NOT NULL,
            paisId INT NOT NULL,
            FOREIGN KEY (paisId) REFERENCES {schema}.pais (id)
        )
    ''')
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {schema}.educacionExterna (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(255) NOT NULL,
            año INT NOT NULL,
            institucionExternaId INT NOT NULL,
            estudianteId INT NOT NULL,
            tipoCarreraId INT NOT NULL,
            FOREIGN KEY (institucionExternaId) REFERENCES {schema}.institucionExterna (id),
            FOREIGN KEY (estudianteId) REFERENCES {schema}.estudiante (id),
            FOREIGN KEY (tipoCarreraId) REFERENCES {schema}.tipoCarrera (id)
        )
    ''')
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {schema}.sector (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(255) NOT NULL
        )
    ''')
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {schema}.tipoEmpresa (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(255) NOT NULL
        )
    ''')
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {schema}.empresa (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(255) NOT NULL,
            correo VARCHAR(255),
            web VARCHAR(255),
            tipoEmpresaId INT NOT NULL,
            sectorId INT NOT NULL,
            FOREIGN KEY (tipoEmpresaId) REFERENCES {schema}.tipoEmpresa (id),
            FOREIGN KEY (sectorId) REFERENCES {schema}.sector (id)
        )
    ''')
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {schema}.trabajoEstudiante (
            id SERIAL PRIMARY KEY,
            fechaInicio DATE NOT NULL,
            fechaFin DATE,
            orden INT,
            cargo VARCHAR(255) NOT NULL,
            añosExperienciaPrevia INT NOT NULL,
            ofertaSie BOOLEAN NOT NULL,
            estudianteId INT NOT NULL,
            empresaId INT NOT NULL,
            FOREIGN KEY (estudianteId) REFERENCES {schema}.estudiante (id),
            FOREIGN KEY (empresaId) REFERENCES {schema}.empresa (id)
        )
    ''')
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {schema}.trabajoEstudianteSalario (
            id SERIAL PRIMARY KEY,
            salario FLOAT NOT NULL,
            trabajoEstudianteId INTEGER NOT NULL,
            FOREIGN KEY (trabajoEstudianteId) REFERENCES {schema}.trabajoEstudiante (id)
        )
    ''')

    print("Tablas creadas.")
    connection.commit()

if __name__ == '__main__':
    create_tables()