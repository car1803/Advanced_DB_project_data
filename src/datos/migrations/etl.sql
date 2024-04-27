-- Extracción, transformación y carga

INSERT INTO esquemadimensional.dTiempo (fecha, year, month, day)
SELECT fechaInicio, EXTRACT(year FROM fechaInicio), EXTRACT(month FROM fechaInicio), EXTRACT(day FROM fechaInicio)
FROM esquemarelacional.trabajoEstudiante t
WHERE NOT EXISTS (
    SELECT 1 FROM esquemadimensional.dTiempo WHERE fecha = t.fechaInicio
) AND fechaInicio IS NOT NULL
UNION
SELECT fechaFin, EXTRACT(year FROM fechaFin), EXTRACT(month FROM fechaFin), EXTRACT(day FROM fechaFin)
FROM esquemarelacional.trabajoEstudiante t
WHERE NOT EXISTS (
    SELECT 1 FROM esquemadimensional.dTiempo WHERE fecha = t.fechaFin
) AND fechaFin IS NOT NULL;


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

INSERT INTO esquemadimensional.dEmpresa (id, nombre, correo, web, nombreSector, nombreTipo, descripcion)
SELECT esquemarelacional.empresa.id, esquemarelacional.empresa.nombre, esquemarelacional.empresa.correo, esquemarelacional.empresa.web, esquemarelacional.sector.nombre AS nombreSector, esquemarelacional.tipoEmpresa.nombre AS nombreTipo, esquemarelacional.empresa.descripcion
FROM esquemarelacional.empresa
JOIN esquemarelacional.sector ON empresa.sectorId = sector.id
JOIN esquemarelacional.tipoEmpresa ON empresa.tipoEmpresaId = tipoEmpresa.id;

INSERT INTO esquemadimensional.hregistrotrabajo (fechaInicioId, fechaFinId, orden, cargo, añosExperienciaPrevia, salarioPromedio, ofertaSie, estudianteId, empresaId)
SELECT ti.id, tf.id, te.orden, te.cargo, te.añosExperienciaPrevia, AVG(tes.salario) AS salarioPromedio, te.ofertaSie, te.estudianteId, te.empresaId
FROM esquemarelacional.trabajoEstudiante te
JOIN esquemarelacional.trabajoEstudianteSalario tes ON te.id = tes.trabajoEstudianteId
JOIN esquemadimensional.dTiempo ti ON te.fechaInicio = ti.fecha
JOIN esquemadimensional.dTiempo tf ON te.fechaFin = tf.fecha
GROUP BY te.id, ti.id, tf.id, te.orden, te.cargo, te.añosExperienciaPrevia, te.ofertaSie, te.estudianteId, te.empresaId;

INSERT INTO esquemadimensional.dTrabajoEstudianteCarrera (trabajoEstudianteId, carreraId)
SELECT distinct hte.id AS trabajoEstudianteId, ee.carreraId
FROM esquemadimensional.hregistrotrabajo hte
JOIN esquemarelacional.estudiante e ON e.id = hte.estudianteid 
JOIN esquemarelacional.egresado ee ON ee.estudianteId = e.id;

INSERT INTO esquemadimensional.dSector (id, nombre)
SELECT id, nombre FROM  esquemarelacional.sector;

INSERT INTO esquemadimensional.dTipoEmpresa (id, nombre)
SELECT id, nombre FROM  esquemarelacional.tipoEmpresa;

INSERT INTO esquemadimensional.dIdioma (id, nombre)
SELECT id, nombre FROM  esquemarelacional.idioma;

INSERT INTO esquemadimensional.dIdiomaNivel (id, nombre)
SELECT id, nombre FROM  esquemarelacional.idiomaNivel;

INSERT INTO esquemadimensional.hregistroestudioidioma (idiomaId, idiomaNivelId, estudianteId)
SELECT idiomaId, idiomaNivelId, estudianteId FROM esquemarelacional.estudianteIdioma;

INSERT INTO esquemadimensional.hregistroempresa (id, nombre, correo, web, tipoEmpresaId, sectorId, gastoEnSalariosTotal, numeroDeEmpleadosTotal, numerodeEmpleadosActual, descripcion)
SELECT
    id,
    nombre,
    correo,
    web,
    tipoEmpresaId,
    sectorId,
    0 AS gastoensalariostotal,
    0 as numeroDeEmpleadosTotal,
    0 as numerodeEmpleadosActual,
    descripcion
FROM esquemarelacional.empresa;

UPDATE esquemadimensional.hregistroempresa h
SET gastoensalariostotal = subquery.total_salario
FROM (
    SELECT h.id, SUM(tes.salario) AS total_salario
    FROM esquemadimensional.hregistroempresa h
    JOIN esquemarelacional.trabajoEstudiante AS te ON te.empresaId = h.id
    JOIN esquemarelacional.trabajoEstudianteSalario AS tes ON tes.trabajoEstudianteId = te.id
    GROUP BY h.id
) AS subquery
WHERE h.id = subquery.id;

UPDATE esquemadimensional.hregistroempresa h
SET numeroDeEmpleadosTotal = subquery.numeroDeEmpleadosTotal
FROM (
    SELECT h.id, count(te.id) AS numeroDeEmpleadosTotal
    FROM esquemadimensional.hregistroempresa h
    JOIN esquemarelacional.trabajoEstudiante AS te ON te.empresaId = h.id
    GROUP BY h.id
) AS subquery
WHERE h.id = subquery.id;

UPDATE esquemadimensional.hregistroempresa h
SET numerodeEmpleadosActual = subquery.numerodeEmpleadosActual
FROM (
    SELECT h.id, count(te.id) AS numerodeEmpleadosActual
    FROM esquemadimensional.hregistroempresa h
    JOIN esquemarelacional.trabajoEstudiante AS te ON te.empresaId = h.id
    WHERE te.fechaFin IS NULL
    GROUP BY h.id
) AS subquery
WHERE h.id = subquery.id;

INSERT INTO esquemadimensional.dEmpresaCarrera (empresaId, carreraId)
select distinct he.id, ee.carreraId
FROM esquemadimensional.hregistroempresa he 
JOIN esquemarelacional.trabajoEstudiante te ON te.empresaId = he.id
JOIN esquemarelacional.estudiante e ON e.id = te.estudianteid 
JOIN esquemarelacional.egresado ee ON ee.estudianteId = e.id;

INSERT INTO esquemadimensional.dEstudianteIdiomaEmpresa (estudianteIdiomaId, empresaId)
SELECT distinct hei.id, te.empresaId
FROM esquemadimensional.hregistroestudioidioma hei
JOIN esquemarelacional.estudiante e ON e.id = hei.estudianteId 
JOIN esquemarelacional.trabajoEstudiante te on te.estudianteId = e.id;

INSERT INTO esquemadimensional.dEstudianteIdiomaCarrera (estudianteIdiomaId, carreraId)
SELECT distinct hei.id, ee.carreraId
FROM esquemadimensional.hregistroestudioidioma hei
JOIN esquemarelacional.estudiante e ON e.id = hei.estudianteId 
JOIN esquemarelacional.egresado ee ON ee.estudianteId = e.id;


