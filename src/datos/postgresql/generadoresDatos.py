from faker import Faker
import random

fake = Faker()

def taskPais(i, __):
    pais = (       
    "United States",
    "Canada",
    "Mexico",
    "Argentina",
    "Brazil",
    "Chile",
    "Colombia",
    "Spain",
    "France",
    "Germany",
    "Italy",
    "United Kingdom"
    )[i % 12]
    return f'''
        INSERT INTO pais (nombre) VALUES ('{pais}');
    '''

def taskDocumento(i,_):
    nombre_documento = ('CC', 'TI', 'CE', 'PA')[i % 4]
    return f'''
        INSERT INTO tipoDocumento (nombre) VALUES ('{nombre_documento}');
    '''

def taskEstudiante(___, __):
    nombre = fake.first_name()
    apellido = fake.last_name()
    correo = fake.email()
    fecha_nacimiento = fake.date_of_birth(minimum_age=18, maximum_age=35)
    genero = fake.random_element(elements=('M', 'F'))
    documento = fake.random_int(min=1000000000, max=9999999999)
    pais_id = fake.random_int(min=1, max=12) 
    tipo_documento_id = fake.random_int(min=1, max=4) 
    return f'''
        INSERT INTO estudiante (nombre, correo, apellido, fechaNacimiento, genero, documento, paisId, tipoDocumentoId) 
        VALUES ('{nombre}', '{correo}', '{apellido}', '{fecha_nacimiento}', '{genero}', {documento}, {pais_id}, {tipo_documento_id});
    '''

def taskTipoCarrera(i, __):
    tipo = (
        "Pregrado",
        "Maestría",
        "Doctorado"
    )[i % 3]
    return f'''
        INSERT INTO tipoCarrera (nombre) VALUES ('{tipo}');
    '''

def taskIdioma(i, __):
    nombre_idioma = (
        "Inglés",
        "Francés",
        "Alemán",
        "Italiano",
        "Portugués",
        "Chino",
    )[i % 6]
    return f'''
        INSERT INTO idioma (nombre) VALUES ('{nombre_idioma}');
    '''

def taskIdiomaNivel(___,__):
    nivel_mapping = {'A1': 1, 'A2': 2, 'B1': 3, 'B2': 4, 'C1': 5, 'C2': 6}
    queries = []
    for nivel, id_nivel in nivel_mapping.items():
        queries.append(f"INSERT INTO idiomaNivel (id, nombre) VALUES ({id_nivel}, '{nivel}');")
    return '\n'.join(queries)

def taskSede(i,__):
    nombre_sede = ("Bogotá", "Medellín", "Manizales", "Palmira", "Amazonia", "Caribe", "Orinoquia", "Tumaco")[i % 8]
    return f'''
        INSERT INTO sede (nombre) VALUES ('{nombre_sede}');
    '''

def taskInstitucionExterna(___, __):
    nombre_institucion = fake.company()
    pais_id = fake.random_int(min=1, max=12)
    return f'''
        INSERT INTO institucionExterna (nombre, paisId) VALUES ('{nombre_institucion}', {pais_id});
    '''

def taskEducacionExterna(___, volumen):
    nombre_educacion = fake.job()
    año = fake.random_int(min=2003, max=2023)
    institucion_externa_id = fake.random_int(min=1, max=10)  
    estudiante_id = fake.random_int(min=1, max=volumen)  
    tipo_carrera_id = fake.random_int(min=1, max=3)
    return '''
        INSERT INTO educacionExterna (nombre, año, institucionExternaId, estudianteId, tipoCarreraId)
        VALUES ('{nombre_educacion}', {año}, {institucion_externa_id}, {estudiante_id}, {tipo_carrera_id});
    '''.format(año=año,estudiante_id=estudiante_id, tipo_carrera_id=tipo_carrera_id, nombre_educacion=nombre_educacion.replace("'", "''"),institucion_externa_id=institucion_externa_id)

def taskSector(i, __):
    nombre_sector = (
        "Tecnología",
        "Salud",
        "Educación",
        "Finanzas",
        "Comercio",
        "Turismo",
        "Transporte",
        "Manufactura",
    ) [i % 8]
    return '''
        INSERT INTO sector (nombre) VALUES ('{nombre_sector}');
    '''.format(nombre_sector=nombre_sector.replace("'", "''"))

def taskTipoEmpresa(i,_):
    nombre_tipo = ('Pública', 'Privada')[i % 2]
    return f'''
        INSERT INTO tipoEmpresa (nombre) VALUES ('{nombre_tipo}');
    '''

def taskEmpresa(___, volumen):
    nombre_empresa = fake.company()
    correo_empresa = fake.company_email()
    web_empresa = fake.url()
    tipo_empresa_id = fake.random_int(min=1, max=2) 
    sector_empresa_id = fake.random_int(min=1, max=8)
    descripcion = fake.text(max_nb_chars=1000)
    return '''
        INSERT INTO empresa (nombre, correo, web, tipoEmpresaId, sectorId, descripcion)
        VALUES ('{nombre_empresa}', '{correo_empresa}', '{web_empresa}', {tipo_empresa_id}, {sector_empresa_id}, '{descripcion}');
    '''.format(nombre_empresa=nombre_empresa.replace("'", "''"), correo_empresa=correo_empresa, web_empresa=web_empresa, tipo_empresa_id=tipo_empresa_id, sector_empresa_id=sector_empresa_id, descripcion=descripcion.replace("'", "''"))


trabajos = [
    "Ingeniero de software",
    "Desarrollador web",
    "Analista de datos",
    "Consultor financiero",
    "Economista",
    "Arquitecto",
    "Ingeniero civil",
    "Ingeniero eléctrico",
    "Ingeniero mecánico",
    "Ingeniero industrial",
    "Diseñador gráfico",
    "Periodista",
    "Fotógrafo",
    "Científico de datos",
    "Investigador",
    "Abogado",
    "Abogado de derechos humanos",
    "Contador",
    "Psicólogo",
    "Veterinario",
    "Médico",
    "Enfermero",
    "Dentista",
    "Farmacéutico",
    "Biólogo",
    "Químico",
    "Profesor",
    "Maestro",
    "Consejero escolar",
    "Analista de sistemas",
    "Programador",
    "Analista de negocios",
    "Gerente de proyecto",
    "Consultor de gestión",
    "Marketing Manager",
    "Recursos Humanos",
    "Gerente de ventas",
    "Especialista en relaciones públicas",
    "Analista financiero",
    "Director de marketing",
    "Analista de mercado",
    "Gerente de producto",
    "Gerente de operaciones",
    "Gerente de calidad",
    "Ingeniero de control de calidad",
    "Diseñador de productos",
    "Gerente de cadena de suministro",
    "Logística y distribución",
    "Gerente de compras",
    "Gerente de producción"
]

fake.job = lambda: random.choice(trabajos)

def taskTrabajoEstudiante(___, volumen):
    random_number = random.random()
    probabilidad_ejecucion = 0.5
    fecha_inicio = fake.date_this_decade()
    if random_number < probabilidad_ejecucion:
        fecha_fin = fake.date_this_decade()
        while fecha_fin <= fecha_inicio:
            fecha_inicio = fake.date_this_decade()
            fecha_fin = fake.date_this_decade()
        fecha_fin = f"'{fecha_fin}'"
    else:   
        fecha_fin = "NULL"

    orden = fake.random_int(min=1, max=volumen)
    cargo = fake.job()
    años_experiencia_previa = fake.random_int(min=0, max=10)
    oferta_sie = fake.boolean()
    estudiante_id = fake.random_int(min=1, max=volumen) 
    empresa_id = fake.random_int(min=1, max=1000) #TODO: este valor está quemado por el número de empresas sería bueno poder parametrisar eso
    return '''
        INSERT INTO trabajoEstudiante (fechaInicio, fechaFin, orden, cargo, añosExperienciaPrevia, ofertaSie, estudianteId, empresaId)
        VALUES ('{fecha_inicio}', {fecha_fin}, {orden}, '{cargo}', {años_experiencia_previa}, {oferta_sie}, {estudiante_id}, {empresa_id});
    '''.format(fecha_inicio=fecha_inicio, fecha_fin=fecha_fin, orden=orden, cargo=cargo.replace("'", "''"), años_experiencia_previa=años_experiencia_previa, oferta_sie=oferta_sie, estudiante_id=estudiante_id, empresa_id=empresa_id)

def taskTrabajoEstudianteSalario(___, volumen):
    salario  = random.uniform(1000000, 15000000)
    trabajoEstudianteId = fake.random_int(min=1, max=volumen) 
    return f'''
        INSERT INTO trabajoEstudianteSalario (salario, trabajoEstudianteId) VALUES ({salario}, {trabajoEstudianteId});
    '''

## 8 sedes x 8 facultades = 64 facultades
def taskFacultad(_, __):
    facultades = [
        "Facultad de Ingeniería",
        "Facultad de Ciencias Sociales",
        "Facultad de Ciencias Económicas",
        "Facultad de Ciencias de la Salud",
        "Facultad de Ciencias de la Educación",
        "Facultad de Ciencias Naturales",
        "Facultad de Ciencias Humanas",
        "Facultad de Ciencias Jurídicas"
    ]
    
    sedes = [
        "Bogotá", "Medellín", "Manizales", "Palmira", "Amazonia", "Caribe", "Orinoquia", "Tumaco"
    ]

    stringquery = ""
    for facultad in facultades:
        for sede_id in range(1, 9):
            stringquery += f"INSERT INTO facultad (nombre, sedeId) VALUES ('{facultad}', {sede_id});\n"

    return stringquery

## 1 departamentos x 64 facultades = 64 departamentos
def taskDepartamento(i, __):
    facultades = [
        "Facultad de Ingeniería",
        "Facultad de Ciencias Sociales",
        "Facultad de Ciencias Económicas",
        "Facultad de Ciencias de la Salud",
        "Facultad de Ciencias de la Educación",
        "Facultad de Ciencias Naturales",
        "Facultad de Ciencias Humanas",
        "Facultad de Ciencias Jurídicas"
    ]
    
    stringquery = ""
    for facultadId in range(1,65):
        stringquery += f"INSERT INTO departamento (nombre, facultadId) VALUES ('Departamento', '{facultadId}' );\n"
    return stringquery

## 3 tipos de carrera x 2 nombres de carrera x 64 departamentos = 384 carreras
def taskCarrera(___, volumen):
    tipos_carrera = ['Pregrado', 'Maestría', 'Doctorado']
    nombres_carrera = ['Carrera 1', 'Carrera 2']
    query = ""
    for tipo in tipos_carrera:
        for nombre in nombres_carrera:
            for departamento_id in range(1, 65):
                nombre_carrera = f'{nombre}'
                tipo_carrera_id = tipos_carrera.index(tipo) + 1  
                query += f'''
                    INSERT INTO carrera (nombre, tipoCarreraId, departamentoId) 
                    VALUES ('{nombre_carrera}', {tipo_carrera_id}, {departamento_id});
                '''
    return query

def taskEgresado(___, volumen):
    año_egreso = fake.random_int(min=2003, max=2023)
    carrera_id = fake.random_int(min=1, max=384)
    estudiante_id = fake.random_int(min=1, max=volumen)
    return f'''
        INSERT INTO egresado (año, carreraId, estudianteId) VALUES ({año_egreso}, {carrera_id}, {estudiante_id});
    '''

def taskEstudianteIdioma(___, volumen):
    idioma_id = fake.random_int(min=1, max=6)
    idioma_nivel_id = fake.random_int(min=1, max=6)
    estudiante_id = fake.random_int(min=1, max=volumen)
    return f'''
        INSERT INTO estudianteIdioma (idiomaId, idiomaNivelId, estudianteId) VALUES ({idioma_id}, {idioma_nivel_id}, {estudiante_id});
    '''