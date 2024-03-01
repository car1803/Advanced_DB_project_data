from faker import Faker
import psycopg2

fake = Faker()

connection = psycopg2.connect(
    host="35.237.42.142",
    database="egresados",
    user="postgres",
    password="665RE(v&x>iVL;6<"
)

cursor = connection.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS pais (
        id SERIAL PRIMARY KEY,
        nombre VARCHAR(255) NOT NULL
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tipoDocumento (
        id SERIAL PRIMARY KEY,
        nombre VARCHAR(255) NOT NULL
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS estudiante (
        id SERIAL PRIMARY KEY,
        nombre VARCHAR(255) NOT NULL,
        correo VARCHAR(255) NOT NULL,
        apellido VARCHAR(255) NOT NULL,
        fechaNacimiento DATE NOT NULL,
        genero VARCHAR(1) NOT NULL,
        documento VARCHAR(255) NOT NULL,
        paisId INT NOT NULL, 
        tipoDocumentoId INT NOT NULL, 
        FOREIGN KEY (paisId) REFERENCES pais (id), 
        FOREIGN KEY (tipoDocumentoId) REFERENCES tipoDocumento (id)
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tipoCarrera (
        id SERIAL PRIMARY KEY, 
        nombre VARCHAR(255) NOT NULL
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS sede (
        id SERIAL PRIMARY KEY,
        nombre VARCHAR(255) NOT NULL
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS facultad (
        id SERIAL PRIMARY KEY,
        nombre VARCHAR(255) NOT NULL,
        sedeId INTEGER NOT NULL,
        FOREIGN KEY (sedeId) REFERENCES sede(id)
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS departamento (
        id SERIAL PRIMARY KEY,
        nombre VARCHAR(255) NOT NULL,
        facultadId INTEGER NOT NULL,
        FOREIGN KEY (facultadId) REFERENCES facultad(id)
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS carrera (
        id SERIAL PRIMARY KEY,
        nombre VARCHAR(255) NOT NULL,
        tipoCarreraId INTEGER NOT NULL,
        departamentoId INTEGER NOT NULL,
        FOREIGN KEY (tipoCarreraId) REFERENCES tipoCarrera(id),
        FOREIGN KEY (departamentoId) REFERENCES departamento(id)
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS egresado (
        id SERIAL PRIMARY KEY,
        año INT NOT NULL,
        carreraId INT NOT NULL,
        estudianteId INT NOT NULL,
        FOREIGN KEY (carreraId) REFERENCES carrera (id),
        FOREIGN KEY (estudianteId) REFERENCES estudiante (id)
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS idioma (
        id SERIAL PRIMARY KEY,
        nombre VARCHAR(255) NOT NULL
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS idiomaNivel (
        id SERIAL PRIMARY KEY,
        nombre VARCHAR(255) NOT NULL
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS estudianteIdioma (
        id SERIAL PRIMARY KEY,
        idiomaId INTEGER REFERENCES idioma(id),
        idiomaNivelId INTEGER REFERENCES idiomaNivel(id),
        estudianteId INTEGER REFERENCES estudiante(id)
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS institucionExterna (
        id SERIAL PRIMARY KEY,
        nombre VARCHAR(255) NOT NULL,
        paisId INT NOT NULL,
        FOREIGN KEY (paisId) REFERENCES pais (id)
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS educacionExterna (
        id SERIAL PRIMARY KEY,
        nombre VARCHAR(255) NOT NULL,
        año INT NOT NULL,
        institucionExternaId INT NOT NULL,
        estudianteId INT NOT NULL,
        tipoCarreraId INT NOT NULL,
        FOREIGN KEY (institucionExternaId) REFERENCES institucionExterna (id),
        FOREIGN KEY (estudianteId) REFERENCES estudiante (id),
        FOREIGN KEY (tipoCarreraId) REFERENCES tipoCarrera (id)
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS sectorEmpresa (
        id SERIAL PRIMARY KEY,
        nombre VARCHAR(255) NOT NULL
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tipoEmpresa (
        id SERIAL PRIMARY KEY,
        nombre VARCHAR(255) NOT NULL
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS empresa (
        id SERIAL PRIMARY KEY,
        nombre VARCHAR(255) NOT NULL,
        correo VARCHAR(255),
        web VARCHAR(255),
        tipoEmpresaId INT NOT NULL,
        sectorEmpresaId INT NOT NULL,
        FOREIGN KEY (tipoEmpresaId) REFERENCES tipoEmpresa (id),
        FOREIGN KEY (sectorEmpresaId) REFERENCES sectorEmpresa (id)
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS trabajoEstudiante (
        id SERIAL PRIMARY KEY,
        fechaInicio DATE NOT NULL,
        fechaFin DATE,
        orden INT,
        cargo VARCHAR(255) NOT NULL,
        añosExperienciaPrevia INT NOT NULL,
        ofertaSie BOOLEAN NOT NULL,
        estudianteId INT NOT NULL,
        empresaId INT NOT NULL,
        FOREIGN KEY (estudianteId) REFERENCES estudiante (id),
        FOREIGN KEY (empresaId) REFERENCES empresa (id)
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS trabajoEstudianteSalario (
        id SERIAL PRIMARY KEY,
        salario FLOAT NOT NULL,
        trabajoEstudianteId INTEGER NOT NULL,
        FOREIGN KEY (trabajoEstudianteId) REFERENCES trabajoEstudiante (id)
    )
''')

# Generar e insertar datos ficticios en la tabla 'pais'
for _ in range(1000):  # Ajusta según la cantidad deseada
    nombre_pais = fake.country()
    cursor.execute('''
        INSERT INTO pais (nombre) VALUES (%s)
    ''', (nombre_pais,))

# Generar e insertar datos ficticios en la tabla 'tipoDocumento'
for _ in range(1000):
    nombre_documento = fake.random_element(elements=("CC","TI","CE","PA"))
    cursor.execute('''
        INSERT INTO tipoDocumento (nombre) VALUES (%s)
    ''', (nombre_documento,))

# Generar e insertar datos ficticios en la tabla 'estudiante'
for _ in range(1000):
    nombre = fake.first_name()
    apellido = fake.last_name()
    correo = fake.email()
    fecha_nacimiento = fake.date_of_birth(minimum_age=18, maximum_age=35)
    genero = fake.random_element(elements=('M', 'F'))
    documento = fake.random_int(min=1000000000, max=9999999999)
    pais_id = fake.random_int(min=1, max=1000) 
    tipo_documento_id = fake.random_int(min=1, max=1000)  
    cursor.execute('''
        INSERT INTO estudiante (nombre, correo, apellido, fechaNacimiento, genero, documento, paisId, tipoDocumentoId) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    ''', (nombre, correo, apellido, fecha_nacimiento, genero, documento, pais_id, tipo_documento_id))

# Generar e insertar datos ficticios en la tabla 'tipoCarrera'
for _ in range(1000):
    nombre_carrera = fake.job()
    cursor.execute('''
        INSERT INTO tipoCarrera (nombre) VALUES (%s)
    ''', (nombre_carrera,))

# Generar e insertar datos ficticios en la tabla 'sede'
for _ in range(1000): 
    nombre_sede = fake.random_element(elements=("Bogotá","Medellín","Manizales","Palmira","Amazonia","Caribe","Orinoquia","Tumaco",))    
    cursor.execute('''
        INSERT INTO sede (nombre) VALUES (%s)
    ''', (nombre_sede,))

# Generar e insertar datos ficticios en la tabla 'facultad'
for _ in range(1000):
    nombre_facultad = fake.word()
    sede_id = fake.random_int(min=1, max=1000) 
    cursor.execute('''
        INSERT INTO facultad (nombre, sedeId) VALUES (%s, %s)
    ''', (nombre_facultad, sede_id))

# Generar e insertar datos ficticios en la tabla 'departamento'
for _ in range(1000):  
    nombre_departamento = fake.word()
    facultad_id = fake.random_int(min=1, max=1000) 
    cursor.execute('''
        INSERT INTO departamento (nombre, facultadId) VALUES (%s, %s)
    ''', (nombre_departamento, facultad_id))

# Generar e insertar datos ficticios en la tabla 'carrera'
for _ in range(1000):  
    nombre_carrera = fake.word()
    tipo_carrera_id = fake.random_int(min=1, max=1000)
    departamento_id = fake.random_int(min=1, max=1000)
    cursor.execute('''
        INSERT INTO carrera (nombre, tipoCarreraId, departamentoId) VALUES (%s, %s, %s)
    ''', (nombre_carrera, tipo_carrera_id, departamento_id))

# Generar e insertar datos ficticios en la tabla 'egresado'
for _ in range(1000):
    año_egreso = fake.random_int(min=1970, max=2024)
    carrera_id = fake.random_int(min=1, max=1000)
    estudiante_id = fake.random_int(min=1, max=1000)
    cursor.execute('''
        INSERT INTO egresado (año, carreraId, estudianteId) VALUES (%s, %s, %s)
    ''', (año_egreso, carrera_id, estudiante_id))

# Generar e insertar datos ficticios en la tabla 'idioma'
for _ in range(1000):
    nombre_idioma = fake.language_name()
    cursor.execute('''
        INSERT INTO idioma (nombre) VALUES (%s)
    ''', (nombre_idioma,))

# Generar e insertar datos ficticios en la tabla 'idiomaNivel'
nivel_mapping = {'A1': 1, 'A2': 2, 'B1': 3, 'B2': 4, 'C1': 5, 'C2': 6}
for nivel, id_nivel in nivel_mapping.items():
    cursor.execute('''
        INSERT INTO idiomaNivel (id, nombre) VALUES (%s, %s)
    ''', (id_nivel, nivel))

# Generar e insertar datos ficticios en la tabla 'estudianteIdioma'
for _ in range(1000):
    idioma_id = fake.random_int(min=1, max=1000)
    idioma_nivel_id = fake.random_int(min=1, max=6)
    estudiante_id = fake.random_int(min=1, max=1000)
    cursor.execute('''
        INSERT INTO estudianteIdioma (idiomaId, idiomaNivelId, estudianteId) VALUES (%s, %s, %s)
    ''', (idioma_id, idioma_nivel_id, estudiante_id))

# Generar e insertar datos ficticios en la tabla 'institucionExterna'
for _ in range(1000):
    nombre_institucion = fake.company()
    pais_id = fake.random_int(min=1, max=1000)
    cursor.execute('''
        INSERT INTO institucionExterna (nombre, paisId) VALUES (%s, %s)
    ''', (nombre_institucion, pais_id))

# Generar e insertar datos ficticios en la tabla 'educacionExterna'
for _ in range(1000):
    nombre_educacion = fake.job()
    año = fake.random_int(min=1990, max=2022)
    institucion_externa_id = fake.random_int(min=1, max=1000)  
    estudiante_id = fake.random_int(min=1, max=1000)  
    tipo_carrera_id = fake.random_int(min=1, max=1000)
    cursor.execute('''
        INSERT INTO educacionExterna (nombre, año, institucionExternaId, estudianteId, tipoCarreraId) VALUES (%s, %s, %s, %s, %s)
    ''', (nombre_educacion, año, institucion_externa_id, estudiante_id, tipo_carrera_id))

# Generar e insertar datos ficticios en la tabla 'sectorEmpresa'
for _ in range(1000):  
    nombre_sector = fake.word()  
    cursor.execute('''
        INSERT INTO sectorEmpresa (nombre) VALUES (%s)
    ''', (nombre_sector,))

# Generar e insertar datos ficticios en la tabla 'tipoEmpresa'
for _ in range(1000):
    nombre_tipo = fake.random_element(elements=('publico', 'privada'))
    cursor.execute('''
        INSERT INTO tipoEmpresa (nombre) VALUES (%s)
    ''', (nombre_tipo,))

# Generar e insertar datos ficticios en la tabla 'empresa'
for _ in range(1000): 
    nombre_empresa = fake.company()
    correo_empresa = fake.company_email()
    web_empresa = fake.url()
    tipo_empresa_id = fake.random_int(min=1, max=1000) 
    sector_empresa_id = fake.random_int(min=1, max=1000)
    cursor.execute('''
        INSERT INTO empresa (nombre, correo, web, tipoEmpresaId, sectorEmpresaId)
        VALUES (%s, %s, %s, %s, %s)
    ''', (nombre_empresa, correo_empresa, web_empresa, tipo_empresa_id, sector_empresa_id))

# Generar e insertar datos ficticios en la tabla 'trabajoEstudiante'
for _ in range(1000):
    fecha_inicio = fake.date_this_decade()
    fecha_fin = fake.date_this_decade()
    while fecha_fin <= fecha_inicio:
        fecha_fin = fake.date_this_decade()
    orden = fake.random_int(min=1, max=1000)
    cargo = fake.job()
    años_experiencia_previa = fake.random_int(min=0, max=10)
    oferta_sie = fake.boolean()
    estudiante_id = fake.random_int(min=1, max=1000) 
    empresa_id = fake.random_int(min=1, max=1000)
    cursor.execute('''
        INSERT INTO trabajoEstudiante (fechaInicio, fechaFin, orden, cargo, añosExperienciaPrevia, ofertaSie, estudianteId, empresaId)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    ''', (fecha_inicio, fecha_fin, orden, cargo, años_experiencia_previa, oferta_sie, estudiante_id, empresa_id))

# Generar e insertar datos ficticios en la tabla 'trabajoEstudianteSalario'
for _ in range(1000):
    salario = fake.random_float(min=1000000, max=5000000)
    trabajoEstudianteId = fake.random_int(min=1, max=1000) 
    cursor.execute('''
        INSERT INTO trabajoEstudianteSalario (salario, trabajoEstudianteId) VALUES (%s, %s)
    ''', (salario, trabajoEstudianteId))

# Confirmar los cambios y cerrar la conexión
connection.commit()
connection.close()