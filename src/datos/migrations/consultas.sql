-- Trabajo
SET search_path TO esquemadimensional;
-- Datos 

-- Duración promedio de un trabajo en días

SELECT AVG(dt_fin.fecha - dt_inicio.fecha) AS duracion_promedio_en_dias
FROM esquemadimensional.hregistrotrabajo he
JOIN esquemadimensional.dTiempo dt_inicio ON he.fechaInicioId = dt_inicio.id
JOIN esquemadimensional.dTiempo dt_fin ON he.fechaFinId = dt_fin.id
WHERE he.fechaFinId IS NOT NULL;

-- Años de experiencia previos promedio de un trabajo

SELECT AVG(añosExperienciaPrevia) AS experiencia_previa_promedio
FROM esquemadimensional.hregistrotrabajo;

-- Número de trabajos promedio de un estudiante

SELECT AVG(num_trabajos) AS num_trabajos_promedio
FROM (
    SELECT estudianteId, COUNT(*) AS num_trabajos
    FROM esquemadimensional.hregistrotrabajo
    GROUP BY estudianteId
) AS trabajos_por_estudiante;

-- Número de trabajos aplicados por SIE

SELECT COUNT(*) AS num_trabajos_SIE
FROM esquemadimensional.hregistrotrabajo
WHERE ofertaSie = true; 

-- Porcentaje de trabajos aplicados por SIE

SELECT (COUNT(CASE WHEN ofertaSie = true THEN 1 END) * 100.0) / COUNT(*) AS porcentaje_trabajos_SIE
FROM esquemadimensional.hregistrotrabajo;

-- Salario promedio de trabajos 

SELECT AVG(salarioPromedio) AS salario_promedio
FROM esquemadimensional.hregistrotrabajo he;

-- Gráficos de barras 

-- Duración promedio en días de trabajo por cargo

SELECT cargo, AVG((dt.fecha - dt_inicio.fecha)) AS duracion_promedio
FROM esquemadimensional.hregistrotrabajo he
JOIN esquemadimensional.dTiempo dt_inicio ON he.fechaInicioId = dt_inicio.id
JOIN esquemadimensional.dTiempo dt ON he.fechaFinId = dt.id
GROUP BY cargo;

-- Salario promedio de trabajo por cargo 

SELECT cargo, AVG(salarioPromedio) AS salario_promedio
FROM esquemadimensional.hregistrotrabajo he
GROUP BY cargo
order by salario_promedio;

-- Número de trabajos por sector empresarial 

SELECT em.nombreSector AS sector_empresa, COUNT(te.id) AS num_trabajos
FROM esquemadimensional.hregistrotrabajo te
JOIN esquemadimensional.dEmpresa em ON te.empresaId = em.id
GROUP BY em.nombreSector
ORDER BY num_trabajos;

-- Número de trabajos por carrera 

SELECT dc.nombrefacultad || ' ' || dc.nombre AS carrera, COUNT(h.id) AS num_trabajos
FROM esquemadimensional.hregistrotrabajo h
JOIN esquemadimensional.dTrabajoEstudianteCarrera t ON h.id = t.trabajoEstudianteId
JOIN esquemadimensional.dCarrera dc ON t.carreraId = dc.id
GROUP BY carrera
ORDER BY num_trabajos;

-- Número de trabajos por facultad 

SELECT dc.nombreFacultad AS facultad, COUNT(h.id) AS num_trabajos
FROM esquemadimensional.hregistrotrabajo h
JOIN esquemadimensional.dTrabajoEstudianteCarrera t ON h.id = t.trabajoEstudianteId
JOIN esquemadimensional.dCarrera dc ON t.carreraId = dc.id
GROUP BY dc.nombreFacultad
ORDER BY num_trabajos;

--Número de trabajos por sede 

SELECT dc.nombreSede AS sede, COUNT(h.id) AS num_trabajos
FROM esquemadimensional.hregistrotrabajo h
JOIN esquemadimensional.dTrabajoEstudianteCarrera t ON h.id = t.trabajoEstudianteId
JOIN esquemadimensional.dCarrera dc ON t.carreraId = dc.id
GROUP BY dc.nombreSede
ORDER BY num_trabajos;

-- Número de trabajos por cargo 

SELECT cargo, COUNT(id) AS num_trabajos
FROM esquemadimensional.hregistrotrabajo
GROUP BY cargo;

-- Gráficos de pastel 

-- Distribución de genero por estudiantes que trabajan

SELECT e.genero, COUNT(te.id) AS num_estudiantes
FROM esquemadimensional.hregistrotrabajo te
INNER JOIN esquemadimensional.dEstudiante e ON te.estudianteId = e.id
GROUP BY e.genero;

-- Gráficos de línea 

-- Número de trabajos por año

SELECT dt.year AS año,
       COUNT(he.id) AS num_trabajos
FROM esquemadimensional.hregistrotrabajo he
JOIN esquemadimensional.dTiempo dt ON he.fechainicioId = dt.id
GROUP BY dt.year
ORDER BY dt.year;

-- Empresa 

-- Datos 

-- Conteo de empresas

SELECT COUNT(id) AS total_empresas
FROM esquemadimensional.hregistroempresa;

-- Gráfico de barras

-- Gasto en salarios por sector 

SELECT se.nombre AS sector_empresa, SUM(he.gastoEnSalariosTotal) AS gasto_salarios
FROM esquemadimensional.hregistroempresa he
JOIN esquemadimensional.dSector se ON he.sectorId = se.id
GROUP BY se.nombre;
 
-- Número de empleados actual por sector 

SELECT se.nombre AS sector_empresa, SUM(he.numerodeEmpleadosActual) AS num_empleados_actual
FROM esquemadimensional.hregistroempresa he
JOIN esquemadimensional.dSector se ON he.sectorId = se.id
GROUP BY se.nombre;

-- Número de empleados por carrera y tipo

SELECT dc.nombre AS carrera, dc.nombretipocarrera AS tipo_carrera, COUNT(*) AS cantidad_empleados
FROM esquemadimensional.hregistroempresa he
INNER JOIN esquemadimensional.dEmpresaCarrera dec ON he.id = dec.empresaId
INNER JOIN esquemadimensional.dCarrera dc ON dec.carreraId = dc.id
GROUP BY dc.nombre, dc.nombretipocarrera;

-- Gasto en salario total por carrera y tipo

SELECT dc.nombre AS carrera, dc.nombretipocarrera AS tipo_carrera, SUM(he.gastoEnSalariosTotal) AS gasto_salarios_total
FROM esquemadimensional.hregistroempresa he
INNER JOIN esquemadimensional.dEmpresaCarrera dec ON he.id = dec.empresaId
INNER JOIN esquemadimensional.dCarrera dc ON dec.carreraId = dc.id
GROUP BY dc.nombre, dc.nombretipocarrera;

-- Número de empleados actuales por empresa

SELECT he.nombre, he.numerodeempleadosactual
FROM esquemadimensional.hregistroempresa he
LIMIT (SELECT COUNT(*) FROM esquemadimensional.hregistroempresa) / 10;

-- Gasto total por empresa

SELECT he.nombre, he.gastoensalariostotal
FROM esquemadimensional.hregistroempresa he
LIMIT (SELECT COUNT(*) FROM esquemadimensional.hregistroempresa) / 10;

-- Gráficos de pastel

-- Distribución por sector 

SELECT se.nombre AS sector_empresa, COUNT(he.id) AS cantidad_empresas
FROM esquemadimensional.hregistroempresa he
JOIN esquemadimensional.dSector se ON he.sectorid = se.id
GROUP BY se.nombre;


-- Número de empleados actual por tipo 

SELECT te.nombre AS tipo_empresa, SUM(he.numerodeEmpleadosActual) AS num_empleados_actual
FROM esquemadimensional.hregistroempresa he
JOIN esquemadimensional.dTipoEmpresa te ON he.tipoEmpresaId = te.id
GROUP BY te.nombre;


-- Distribución por tipo 

SELECT te.nombre AS tipo_empresa, COUNT(he.id) AS cantidad_empresas
FROM esquemadimensional.hregistroempresa he
JOIN esquemadimensional.dTipoEmpresa te ON he.tipoEmpresaId = te.id
GROUP BY te.nombre;

-- Gasto en salarios por tipo 

SELECT te.nombre AS tipo_empresa, SUM(he.gastoEnSalariosTotal) AS gasto_salarios
FROM esquemadimensional.hregistroempresa he
JOIN esquemadimensional.dTipoEmpresa te ON he.tipoEmpresaId = te.id
GROUP BY te.nombre;

-- Idioma 

-- Datos 

-- Número de idiomas

SELECT COUNT(DISTINCT idiomaid) AS total_idiomas
FROM esquemadimensional.hregistroestudioidioma;

-- Gráfico de barras

-- Número de idiomas por empresa

SELECT de.nombre AS nombre_empresa, COUNT(DISTINCT he.idiomaId) AS numero_idiomas
FROM esquemadimensional.hregistroestudioidioma he
INNER JOIN esquemadimensional.dEstudianteIdiomaEmpresa des ON he.id = des.estudianteIdiomaId
INNER JOIN esquemadimensional.dEmpresa de ON des.empresaId = he.id
GROUP BY de.nombre
limit 100;

-- Nivel de idioma 

select id as nivel, nombre 
from esquemadimensional.didiomanivel d;

-- Nivel promedio de idioma principal por empresa 

SELECT dem.nombre AS nombre_empresa, AVG(hes.idiomaNivelId) AS nivel_promedio_idioma
FROM esquemadimensional.hregistroestudioidioma hes
INNER JOIN (
    SELECT estudianteId, MAX(idiomaNivelId) AS idiomaNivelId
    FROM esquemadimensional.hregistroestudioidioma
    GROUP BY estudianteId
) AS max_nivel ON hes.estudianteId = max_nivel.estudianteId AND hes.idiomaNivelId = max_nivel.idiomaNivelId
INNER JOIN esquemadimensional.dEstudianteIdiomaEmpresa des ON hes.id = des.estudianteIdiomaId
INNER JOIN esquemadimensional.dEmpresa dem ON des.empresaId = dem.id
GROUP BY dem.nombre;

-- Nivel promedio de idioma principal por sector 

SELECT dem.nombreSector AS nombre_sector, AVG(hes.idiomaNivelId) AS nivel_promedio_idioma
FROM esquemadimensional.hregistroestudioidioma hes
INNER JOIN (
    SELECT estudianteId, MAX(idiomaNivelId) AS idiomaNivelId
    FROM esquemadimensional.hregistroestudioidioma
    GROUP BY estudianteId
) AS max_nivel ON hes.estudianteId = max_nivel.estudianteId AND hes.idiomaNivelId = max_nivel.idiomaNivelId
INNER JOIN esquemadimensional.dEstudianteIdiomaEmpresa des ON hes.id = des.estudianteIdiomaId
INNER JOIN esquemadimensional.dEmpresa dem ON des.empresaId = dem.id
GROUP BY dem.nombreSector;

-- Número de idiomas por tipo de carrera

SELECT dca.nombreTipoCarrera AS tipo_carrera, COUNT(DISTINCT hes.idiomaId) AS numero_idiomas
FROM esquemadimensional.hregistroestudioidioma hes
INNER JOIN esquemadimensional.dEstudianteIdiomaCarrera des ON hes.id = des.estudianteIdiomaId
INNER JOIN esquemadimensional.dCarrera dca ON des.carreraId = dca.id
GROUP BY dca.nombreTipoCarrera;

-- Nivel promedio de idioma principal por tipo carrera 

SELECT dca.nombreTipoCarrera AS tipo_carrera, AVG(hes.idiomaNivelId) AS nivel_promedio_idioma
FROM esquemadimensional.hregistroestudioidioma hes
INNER JOIN (
    SELECT estudianteId, MAX(idiomaNivelId) AS idiomaNivelId
    FROM esquemadimensional.hregistroestudioidioma
    GROUP BY estudianteId
) AS max_nivel ON hes.estudianteId = max_nivel.estudianteId AND hes.idiomaNivelId = max_nivel.idiomaNivelId
INNER JOIN esquemadimensional.dEstudianteIdiomaCarrera des ON hes.id = des.estudianteIdiomaId
INNER JOIN esquemadimensional.dCarrera dca ON des.carreraId = dca.id
GROUP BY dca.nombreTipoCarrera;

-- Distribución de nivel por idioma

SELECT did.nombre AS idioma, din.nombre AS nivel, COUNT(hes.id) AS cantidad_estudiantes
FROM esquemadimensional.hregistroestudioidioma hes
INNER JOIN esquemadimensional.dIdioma did ON hes.idiomaId = did.id
INNER JOIN esquemadimensional.dIdiomaNivel din ON hes.idiomaNivelId = din.id
GROUP BY did.nombre, din.nombre;