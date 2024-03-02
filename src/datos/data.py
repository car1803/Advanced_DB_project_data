from src.connectors.connection import connection
from src.utils.taskexcec import taskInsert
from src.connectors.postgresqlcredenciales import schema
from src.datos.generadoresDatos import taskEstudianteIdioma, taskInstitucionExterna, taskCarrera, taskDepartamento, taskFacultad, taskEgresado,taskInstitucionExterna, taskPais,taskIdioma, taskIdiomaNivel, taskDocumento, taskEstudiante, taskTipoCarrera, taskSede, taskEducacionExterna, taskSector, taskTipoEmpresa, taskEmpresa, taskTrabajoEstudiante, taskTrabajoEstudianteSalario

cursor = connection.cursor()
volumen = 100000

def populate_tables(schema="testmodel"):
    print("Generando e insertando datos ficticios en las tablas...")

    # Generar e insertar datos ficticios en la tabla 'pais'
    taskInsert(taskPais, 201, connection,cursor, 200)
    print("Datos insertados en la tabla 'pais'.")

    # Generar e insertar datos ficticios en la tabla 'tipoDocumento'
    taskInsert(taskDocumento, 4, connection, cursor, 1)
    print("Datos insertados en la tabla 'pais'.")

    # Generar e insertar datos ficticios en la tabla 'estudiante'
    taskInsert(taskEstudiante, volumen, connection, cursor, 1000)
    print("Datos insertados en la tabla 'estudiante'.")

    taskInsert(taskTipoCarrera, volumen, connection, cursor, 1000)
    print("Datos insertados en la tabla 'tipoCarrera'.")
    
    taskInsert(taskIdioma, volumen, connection, cursor, 1000)
    print("Datos insertados en la tabla 'idioma'.")

        # Generar e insertar datos ficticios en la tabla 'idiomaNivel'
    taskInsert(taskIdiomaNivel, 6, connection, cursor, 6)
    print("Datos insertados en la tabla 'idiomaNivel'.")

    # Insertar datos específicos en la tabla 'sede'
    taskInsert(taskSede, 7, connection, cursor, 7)
    print("Datos insertados en la tabla 'sede'.")

    # Generar e insertar datos ficticios en la tabla 'educacionExterna'
    taskInsert(taskEducacionExterna, volumen, connection, cursor, 1000)
    print("Datos insertados en la tabla 'educacionExterna'.")

    # Generar e insertar datos ficticios en la tabla 'sector'
    taskInsert(taskSector, volumen, connection, cursor, 1000)
    print("Datos insertados en la tabla 'sector'.")

    # Generar e insertar datos ficticios en la tabla 'tipoEmpresa'
    taskInsert(taskTipoEmpresa, 2, connection, cursor, 1)
    print("Datos insertados en la tabla 'tipoEmpresa'.")

    # Generar e insertar datos ficticios en la tabla 'empresa'
    taskInsert(taskEmpresa, volumen, connection, cursor, 1000)
    print("Datos insertados en la tabla 'empresa'.")

    # Generar e insertar datos ficticios en la tabla 'trabajoEstudiante'
    taskInsert(taskTrabajoEstudiante, volumen, connection, cursor, 1000)
    print("Datos insertados en la tabla 'trabajoEstudiante'.")

    # Generar e insertar datos ficticios en la tabla 'trabajoEstudianteSalario'
    taskInsert(taskTrabajoEstudianteSalario, volumen, connection, cursor, 1000)
    print("Datos insertados en la tabla 'trabajoEstudianteSalario'.")

    # Generar e insertar datos ficticios en la tabla 'facultad'
    taskInsert(taskFacultad, volumen, connection, cursor, 1000)
    print("Datos insertados en la tabla 'facultad'.")

    # Generar e insertar datos ficticios en la tabla 'departamento'
    taskInsert(taskDepartamento, volumen, connection, cursor, 1000)
    print("Datos insertados en la tabla 'departamento'.")

    # Generar e insertar datos ficticios en la tabla 'carrera'
    taskInsert(taskCarrera, volumen, connection, cursor, 1000)
    print("Datos insertados en la tabla 'carrera'.")

    # Generar e insertar datos ficticios en la tabla 'egresado'
    taskInsert(taskEgresado, volumen, connection, cursor, 1000)
    print("Datos insertados en la tabla 'egresado'.")

    # Generar e insertar datos ficticios en la tabla 'estudianteIdioma'
    taskInsert(taskEstudianteIdioma, volumen, connection, cursor, 1000)
    print("Datos insertados en la tabla 'estudianteIdioma'.")

    # Generar e insertar datos ficticios en la tabla 'institucionExterna'
    taskInsert(taskInstitucionExterna, volumen, connection, cursor, 1000)
    print("Datos insertados en la tabla 'institucionExterna'.")

    # Confirmar los cambios y cerrar la conexión
    connection.commit()
