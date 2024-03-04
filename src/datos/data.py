from src.connectors.connection import connection
from src.utils.taskexcec import taskInsert
from src.datos.generadoresDatos import taskEstudianteIdioma, taskInstitucionExterna, taskCarrera, taskDepartamento, taskFacultad, taskEgresado,taskInstitucionExterna, taskPais,taskIdioma, taskIdiomaNivel, taskDocumento, taskEstudiante, taskTipoCarrera, taskSede, taskEducacionExterna, taskSector, taskTipoEmpresa, taskEmpresa, taskTrabajoEstudiante, taskTrabajoEstudianteSalario

cursor = connection.cursor()

def populate_tables(volumen = 100000 + 1, factor = 1000):
    print("Generando e insertando datos ficticios en las tablas...")

    # Generar e insertar datos ficticios en la tabla 'pais'
    print("Datos insertados en la tabla 'pais'.")
    taskInsert(taskPais, 12, connection, cursor, 1)

    # Generar e insertar datos ficticios en la tabla 'tipoDocumento'
    print("Datos insertados en la tabla 'tipoDocumento'.")
    taskInsert(taskDocumento, 4, connection, cursor, 1)

    # Generar e insertar datos ficticios en la tabla 'estudiante'
    print("Datos insertados en la tabla 'estudiante'.")
    taskInsert(taskEstudiante, volumen, connection, cursor, factor)

    print("Datos insertados en la tabla 'tipoCarrera'.")
    taskInsert(taskTipoCarrera, 3, connection, cursor, 1)
    
    print("Datos insertados en la tabla 'idioma'.")
    taskInsert(taskIdioma, 6, connection, cursor, 1)

    # Generar e insertar datos ficticios en la tabla 'idiomaNivel'
    print("Datos insertados en la tabla 'idiomaNivel'.")
    taskInsert(taskIdiomaNivel, 1, connection, cursor, 1)

    # Insertar datos específicos en la tabla 'sede'
    print("Datos insertados en la tabla 'sede'.")
    taskInsert(taskSede, 8, connection, cursor, 7)

    # Generar e insertar datos ficticios en la tabla 'institucionExterna'
    print("Datos insertados en la tabla 'institucionExterna'.")
    taskInsert(taskInstitucionExterna, 10, connection, cursor, 1)

    # Generar e insertar datos ficticios en la tabla 'educacionExterna'
    print("Datos insertados en la tabla 'educacionExterna'.")
    taskInsert(taskEducacionExterna, volumen, connection, cursor, factor)

    # Generar e insertar datos ficticios en la tabla 'sector'
    print("Datos insertados en la tabla 'sector'.")
    taskInsert(taskSector, 8, connection, cursor, 1)

    # Generar e insertar datos ficticios en la tabla 'tipoEmpresa'
    print("Datos insertados en la tabla 'tipoEmpresa'.")
    taskInsert(taskTipoEmpresa, 2, connection, cursor, 1)

    # Generar e insertar datos ficticios en la tabla 'empresa'
    print("Datos insertados en la tabla 'empresa'.")
    taskInsert(taskEmpresa, 1001, connection, cursor, 100)

    # Generar e insertar datos ficticios en la tabla 'trabajoEstudiante'
    print("Datos insertados en la tabla 'trabajoEstudiante'.")
    taskInsert(taskTrabajoEstudiante, volumen, connection, cursor, factor)

    # Generar e insertar datos ficticios en la tabla 'trabajoEstudianteSalario'
    print("Datos insertados en la tabla 'trabajoEstudianteSalario'.")
    taskInsert(taskTrabajoEstudianteSalario, volumen, connection, cursor, factor)

    # Generar e insertar datos ficticios en la tabla 'facultad'
    print("Datos insertados en la tabla 'facultad'.")
    taskInsert(taskFacultad, 1, connection, cursor, 1)

    # Generar e insertar datos ficticios en la tabla 'departamento'
    print("Datos insertados en la tabla 'departamento'.")
    taskInsert(taskDepartamento, 8, connection, cursor, 1)

    # Generar e insertar datos ficticios en la tabla 'carrera'
    print("Datos insertados en la tabla 'carrera'.")
    taskInsert(taskCarrera, 1, connection, cursor, 1)

    # Generar e insertar datos ficticios en la tabla 'egresado'
    print("Datos insertados en la tabla 'egresado'.")
    taskInsert(taskEgresado, volumen, connection, cursor, factor)

    # Generar e insertar datos ficticios en la tabla 'estudianteIdioma'
    print("Datos insertados en la tabla 'estudianteIdioma'.")
    taskInsert(taskEstudianteIdioma, volumen, connection, cursor, factor)

    # Confirmar los cambios y cerrar la conexión
    connection.commit()
    print("Datos insertados en todas las tablas.")
