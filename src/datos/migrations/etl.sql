-- Extracción, transformación y carga

INSERT INTO esquemadimensional.dTiempo (fecha, year, month, day)
SELECT fechaInicio, EXTRACT(year FROM fechaInicio), EXTRACT(month FROM fechaInicio), EXTRACT(day FROM fechaInicio)
FROM esquemarelacional.trabajoEstudiante t
WHERE NOT EXISTS (
    SELECT 1 FROM esquemadimensional.dTiempo WHERE fecha = t.fechaInicio
)
UNION
SELECT fechaFin, EXTRACT(year FROM fechaFin), EXTRACT(month FROM fechaFin), EXTRACT(day FROM fechaFin)
FROM esquemarelacional.trabajoEstudiante t
WHERE NOT EXISTS (
    SELECT 1 FROM esquemadimensional.dTiempo WHERE fecha = t.fechaFin
);

INSERT INTO esquemadimensional.dEstudiante (id, nombre, correo, apellido, fechaNacimiento, genero, documento, nombrePais, nombreTipoDocumento)
SELECT esquemarelacional.estudiante.id, esquemarelacional.estudiante.nombre, esquemarelacional.estudiante.correo, esquemarelacional.estudiante.apellido, esquemarelacional.estudiante.fechaNacimiento, esquemarelacional.estudiante.genero, esquemarelacional.estudiante.documento, esquemarelacional.pais.nombre AS nombrePais, esquemarelacional.tipoDocumento.nombre AS nombreTipoDocumento
FROM esquemarelacional.estudiante
JOIN esquemarelacional.pais ON estudiante.paisId = pais.id
JOIN esquemarelacional.tipoDocumento ON estudiante.tipoDocumentoId = tipoDocumento.id;

INSERT INTO esquemadimensional.dCarrera (id, nombre, nombreTipoCarrera, nombreDepartamento, nombreFacultad, nombreSede)
SELECT esquemarelacional.carrera.id, esquemarelacional.carrera.nombre, esquemarelacional.tipoCarrera.nombre AS nombreTipoCarrera, esquemarelacional.departamento.nombre AS nombreDepartamento, esquemarelacional.facultad.nombre AS nombreFacultad, esquemarelacional.sede.nombre AS nombreSede
FROM esquemarelacional.carrera
JOIN esquemarelacional.tipoCarrera ON carrera.tipoCarreraId = tipoCarrera.id
JOIN esquemarelacional.departamento ON carrera.departamentoId = departamento.id
JOIN esquemarelacional.facultad ON departamento.facultadId = facultad.id
JOIN esquemarelacional.sede ON facultad.sedeId = sede.id;

INSERT INTO esquemadimensional.dEmpresa (id, nombre, correo, web, nombreSector, nombreTipo)
SELECT esquemarelacional.empresa.id, esquemarelacional.empresa.nombre, esquemarelacional.empresa.correo, esquemarelacional.empresa.web, esquemarelacional.sector.nombre AS nombreSector, esquemarelacional.tipoEmpresa.nombre AS nombreTipo
FROM esquemarelacional.empresa
JOIN esquemarelacional.sector ON empresa.sectorId = sector.id
JOIN esquemarelacional.tipoEmpresa ON empresa.tipoEmpresaId = tipoEmpresa.id;

INSERT INTO esquemadimensional.hTrabajoEstudiante (fechaInicioId, fechaFinId, orden, cargo, añosExperienciaPrevia, salarioPromedio, ofertaSie, estudianteId, empresaId)
SELECT ti.id, tf.id, te.orden, te.cargo, te.añosExperienciaPrevia, AVG(tes.salario) AS salarioPromedio, te.ofertaSie, te.estudianteId, te.empresaId
FROM esquemarelacional.trabajoEstudiante te
JOIN esquemarelacional.trabajoEstudianteSalario tes ON te.id = tes.trabajoEstudianteId
JOIN esquemadimensional.dTiempo ti ON te.fechaInicio = ti.fecha
JOIN esquemadimensional.dTiempo tf ON te.fechaFin = tf.fecha
GROUP BY te.id, ti.id, tf.id, te.orden, te.cargo, te.añosExperienciaPrevia, te.ofertaSie, te.estudianteId, te.empresaId;

INSERT INTO esquemadimensional.dTrabajoEstudianteCarrera (trabajoEstudianteId, carreraId)
SELECT hte.id AS trabajoEstudianteId, ee.carreraId
FROM esquemadimensional.hTrabajoEstudiante hte
JOIN esquemarelacional.estudiante e ON e.id = hte.estudianteid 
JOIN esquemarelacional.egresado ee ON ee.estudianteId = e.id;

INSERT INTO esquemadimensional.dSector (id, nombre)
SELECT id, nombre FROM  esquemarelacional.sector;

INSERT INTO esquemadimensional.dTipoEmpresa (id, nombre)
SELECT id, nombre FROM  esquemarelacional.tipoEmpresa;

INSERT INTO esquemadimensional.hEmpresa (id, nombre, correo, web, tipoEmpresaId, sectorId, gastoEnSalariosTotal, numeroDeEmpleadosTotal, numerodeEmpleadosActual)
SELECT 
	e.id,
    e.nombre,
    e.correo,
    e.web,
    e.tipoEmpresaId,
    e.sectorId,
    COALESCE((
        SELECT SUM(tes.salario)
        FROM  esquemarelacional.trabajoEstudianteSalario AS tes
        JOIN  esquemarelacional.trabajoEstudiante AS te ON tes.trabajoEstudianteId = te.id
        WHERE te.empresaId = e.id
    ), 0) AS gastoEnSalariosTotal,
    COALESCE((
        SELECT COUNT(DISTINCT(te.id))
        FROM  esquemarelacional.trabajoEstudiante AS te
        WHERE te.empresaId = e.id
    ), 0) AS numeroDeEmpleadosTotal,
    COALESCE((
        SELECT COUNT(DISTINCT(te.id))
        FROM  esquemarelacional.trabajoEstudiante AS te
        WHERE te.empresaId = e.id
        AND te.fechaFin IS NULL
    ), 0) AS numerodeEmpleadosActual
FROM  esquemarelacional.empresa AS e
GROUP BY e.id;  

INSERT INTO esquemadimensional.dEmpresaCarrera (empresaId, carreraId)
SELECT he.id, ee.carreraId
FROM esquemadimensional.hEmpresa he 
JOIN esquemarelacional.trabajoEstudiante te ON te.empresaId = he.id
JOIN esquemarelacional.estudiante e ON e.id = te.estudianteid 
JOIN esquemarelacional.egresado ee ON ee.estudianteId = e.id;

INSERT INTO esquemadimensional.dIdioma (id, nombre)
SELECT id, nombre FROM  esquemarelacional.idioma;

INSERT INTO esquemadimensional.dIdiomaNivel (id, nombre)
SELECT id, nombre FROM  esquemarelacional.idiomaNivel;

INSERT INTO esquemadimensional.hEstudianteIdioma (idiomaId, idiomaNivelId, estudianteId)
SELECT idiomaId, idiomaNivelId, estudianteId FROM estudianteIdioma;

INSERT INTO esquemadimensional.dEstudianteIdiomaEmpresa (estudianteIdiomaId, empresaId)
SELECT hei.id, te.empresaId
FROM esquemadimensional.hEstudianteIdioma hei
JOIN esquemarelacional.estudiante e ON e.id = hei.estudianteId 
JOIN esquemarelacional.trabajoEstudiante te on te.estudianteId = e.id;

INSERT INTO esquemadimensional.dEstudianteIdiomaCarrera (estudianteIdiomaId, carreraId)
SELECT hei.id, ee.carreraId
FROM esquemadimensional.hEstudianteIdioma hei
JOIN esquemarelacional.estudiante e ON e.id = hei.estudianteId 
JOIN esquemarelacional.egresado ee ON ee.estudianteId = e.id;


