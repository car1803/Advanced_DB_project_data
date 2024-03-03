-- Extracción, transformación y carga

INSERT INTO dTiempo (fecha, year, month, day)
SELECT fechaInicio, EXTRACT(year FROM fechaInicio), EXTRACT(month FROM fechaInicio), EXTRACT(day FROM fechaInicio)
FROM trabajoEstudiante t
WHERE NOT EXISTS (
    SELECT 1 FROM dTiempo WHERE fecha = t.fechaInicio
)
UNION
SELECT fechaFin, EXTRACT(year FROM fechaFin), EXTRACT(month FROM fechaFin), EXTRACT(day FROM fechaFin)
FROM trabajoEstudiante t
WHERE NOT EXISTS (
    SELECT 1 FROM dTiempo WHERE fecha = t.fechaFin
);

INSERT INTO dEstudiante (id, nombre, correo, apellido, fechaNacimiento, genero, documento, nombrePais, nombreTipoDocumento)
SELECT estudiante.id, estudiante.nombre, estudiante.correo, estudiante.apellido, estudiante.fechaNacimiento, estudiante.genero, estudiante.documento, pais.nombre AS nombrePais, tipoDocumento.nombre AS nombreTipoDocumento
FROM estudiante
JOIN pais ON estudiante.paisId = pais.id
JOIN tipoDocumento ON estudiante.tipoDocumentoId = tipoDocumento.id;

INSERT INTO dCarrera (id, nombre, nombreTipoCarrera, nombreDepartamento, nombreFacultad, nombreSede)
SELECT carrera.id, carrera.nombre, tipoCarrera.nombre AS nombreTipoCarrera, departamento.nombre AS nombreDepartamento, facultad.nombre AS nombreFacultad, sede.nombre AS nombreSede
FROM carrera
JOIN tipoCarrera ON carrera.tipoCarreraId = tipoCarrera.id
JOIN departamento ON carrera.departamentoId = departamento.id
JOIN facultad ON departamento.facultadId = facultad.id
JOIN sede ON facultad.sedeId = sede.id;

INSERT INTO dEmpresa (id, nombre, correo, web, nombreSector, nombreTipo)
SELECT empresa.id, empresa.nombre, empresa.correo, empresa.web, sector.nombre AS nombreSector, tipoEmpresa.nombre AS nombreTipo
FROM empresa
JOIN sector ON empresa.sectorId = sector.id
JOIN tipoEmpresa ON empresa.tipoEmpresaId = tipoEmpresa.id;

INSERT INTO hTrabajoEstudiante (fechaInicioId, fechaFinId, orden, cargo, añosExperienciaPrevia, salarioPromedio, ofertaSie, estudianteId, empresaId)
SELECT ti.id, tf.id, te.orden, te.cargo, te.añosExperienciaPrevia, AVG(tes.salario) AS salarioPromedio, te.ofertaSie, te.estudianteId, te.empresaId
FROM trabajoEstudiante te
JOIN trabajoEstudianteSalario tes ON te.id = tes.trabajoEstudianteId
JOIN dTiempo ti ON te.fechaInicio = ti.fecha
JOIN dTiempo tf ON te.fechaFin = tf.fecha
GROUP BY te.id, ti.id, tf.id, te.orden, te.cargo, te.añosExperienciaPrevia, te.ofertaSie, te.estudianteId, te.empresaId;

INSERT INTO dTrabajoEstudianteCarrera (trabajoEstudianteId, carreraId)
SELECT hte.id AS trabajoEstudianteId, ee.carreraId
FROM hTrabajoEstudiante hte
JOIN estudiante e ON e.id = hte.estudianteid 
JOIN egresado ee ON ee.estudianteId = e.id;

INSERT INTO dSector (id, nombre)
SELECT id, nombre FROM sector;

INSERT INTO dTipoEmpresa (id, nombre)
SELECT id, nombre FROM tipoEmpresa;

INSERT INTO hEmpresa (id, nombre, correo, web, tipoEmpresaId, sectorId, gastoEnSalariosTotal, numeroDeEmpleadosTotal, numerodeEmpleadosActual)
SELECT 
	e.id,
    e.nombre,
    e.correo,
    e.web,
    e.tipoEmpresaId,
    e.sectorId,
    COALESCE((
        SELECT SUM(tes.salario)
        FROM trabajoEstudianteSalario AS tes
        JOIN trabajoEstudiante AS te ON tes.trabajoEstudianteId = te.id
        WHERE te.empresaId = e.id
    ), 0) AS gastoEnSalariosTotal,
    COALESCE((
        SELECT COUNT(DISTINCT(te.id))
        FROM trabajoEstudiante AS te
        WHERE te.empresaId = e.id
    ), 0) AS numeroDeEmpleadosTotal,
    COALESCE((
        SELECT COUNT(DISTINCT(te.id))
        FROM trabajoEstudiante AS te
        WHERE te.empresaId = e.id
        AND te.fechaFin IS NULL
    ), 0) AS numerodeEmpleadosActual
FROM empresa AS e
GROUP BY e.id;  

INSERT INTO dEmpresaCarrera (empresaId, carreraId)
SELECT he.id, ee.carreraId
FROM hEmpresa he 
JOIN trabajoEstudiante te ON te.empresaId = he.id
JOIN estudiante e ON e.id = te.estudianteid 
JOIN egresado ee ON ee.estudianteId = e.id;

INSERT INTO dIdioma (id, nombre)
SELECT id, nombre FROM idioma;

INSERT INTO dIdiomaNivel (id, nombre)
SELECT id, nombre FROM idiomaNivel;

INSERT INTO hEstudianteIdioma (idiomaId, idiomaNivelId, estudianteId)
SELECT idiomaId, idiomaNivelId, estudianteId FROM estudianteIdioma;

INSERT INTO dEstudianteIdiomaEmpresa (estudianteIdiomaId, empresaId)
SELECT hei.id, te.empresaId
FROM hEstudianteIdioma hei
JOIN estudiante e ON e.id = hei.estudianteId 
JOIN trabajoEstudiante te on te.estudianteId = e.id;

INSERT INTO dEstudianteIdiomaCarrera (estudianteIdiomaId, carreraId)
SELECT hei.id, ee.carreraId
FROM hEstudianteIdioma hei
JOIN estudiante e ON e.id = hei.estudianteId 
JOIN egresado ee ON ee.estudianteId = e.id;