drop table if exists dTrabajoEstudianteCarrera;
drop table if exists dEmpresaCarrera;
drop table if exists dEstudianteIdiomaEmpresa; 
drop table if exists hTrabajoEstudiante;
drop table if exists hEmpresa; 
drop table if exists hEstudianteIdioma;
drop table if exists dTiempo;
drop table if exists dEstudiante;
drop table if exists dEmpresa;
drop table if exists dCarrera;
drop table if exists dTrabajoEstudianteCarrera;
drop table if exists dSector; 
drop table if exists dTipoEmpresa; 
drop table if exists dIdioma; 
drop table if exists dIdiomaNivel; 

-- Hecho trabajoEstudiante
-- Es el hecho de los trabajos obtenidos por los estudiantes,
-- proporcionan medidas de información detallada sobre el tiempo, el cargo,
-- la experiencia previa, salario promedio y si se aplicó a través del SIA.

create table dTiempo (
    id serial primary key,
    fecha date not null,
    year int not null,
    month int not null,
    day int not null
);

create table dEstudiante (
    id serial primary key,
    nombre varchar(255) not null,
    correo varchar(255) not null,
	apellido varchar(255) not null,
    fechaNacimiento date not null,
    genero varchar(1) not null,
    documento varchar(255) not null, 
    nombrePais varchar(255) not null,
    nombreTipoDocumento varchar(255) not null
);

create table dEmpresa (
	id serial primary key,
	nombre varchar(255) not null, 
	correo varchar(255) not null, 
	web varchar(255), 
	nombreSector varchar(255) not null, 
	nombreTipo varchar(255) not null
);

create table dCarrera (
	id serial primary key,
	nombre varchar(255) not null, 
	nombreTipoCarrera varchar(255) not null, 
	nombreDepartamento varchar(255) not null, 
	nombreFacultad varchar(255) not null, 
	nombreSede varchar(255) not null
);

create table hTrabajoEstudiante (
	id serial primary key, 
	fechaInicioId int not null, 
	fechaFinId int, 
	orden int,
	cargo varchar(255) not null, 
	añosExperienciaPrevia int not null, 
	salarioPromedio float not null,
	ofertaSie boolean not null,
	estudianteId int not null, 
    empresaId int not null,
    foreign key (fechaInicioId) references dTiempo(id), 
    foreign key (fechaFinId) references dTiempo(id), 
    foreign key (estudianteId) references dEstudiante(id), 
    foreign key (empresaId) references dEmpresa(id)
); 

create table dTrabajoEstudianteCarrera (
    trabajoEstudianteId int not null,
    carreraId int not null,
    primary key (trabajoEstudianteId, carreraId),
    foreign key (trabajoEstudianteId) references hTrabajoEstudiante(id),
    foreign key (carreraId) references dCarrera(id)
);

-- Hecho empresa
-- Es el hecho de las empresas,
-- proporcionan medidas de información detallada sobre el gasto, 
-- sectores, tipos, número de empleados.

create table dSector(
	id serial primary key, 
	nombre varchar(255) not null
); 

create table dTipoEmpresa (
	id serial primary key, 
	nombre varchar(255) not null
); 

create table hEmpresa (
	id serial primary key,
	nombre varchar(255) not null, 
	correo varchar(255), 
	web varchar(255), 
	tipoEmpresaId int not null, 
    sectorId int not null, 
    gastoEnSalariosTotal float not null, 
    numeroDeEmpleadosTotal int not null, 
    numerodeEmpleadosActual int not null,
    foreign key (sectorId) references dSector(id),
    foreign key (tipoEmpresaId) references dTipoEmpresa(id)
);

create table dEmpresaCarrera (
    empresaId int not null,
    carreraId int not null,
    primary key (empresaId, carreraId),
    foreign key (empresaId) references hEmpresa(id),
    foreign key (carreraId) references dCarrera(id)
);

-- Hecho habilidadIdioma
-- Es el hecho de las habilidades con idioma,
-- proporcionan medidas de información sobre los estudiantes, 
-- idiomas, niveles y empresas.

create table dIdioma (
	id serial primary key, 
	nombre varchar(255) not null
); 

create table dIdiomaNivel (
	id serial primary key, 
	nombre varchar(255) not null
); 

create table hEstudianteIdioma (
	id serial primary key,
	idiomaId int not null,
    idiomaNivelId int not null,
    estudianteId int not null,
    foreign key (idiomaId) references dIdioma(id),
    foreign key (idiomaNivelId) references dIdiomaNivel(id), 
    foreign key (estudianteId) references dEstudiante(id)
);

create table dEstudianteIdiomaEmpresa (
    estudianteIdiomaId int not null,
    empresaId int not null,
    primary key (empresaId, estudianteIdiomaId),
    foreign key (empresaId) references dEmpresa(id),
    foreign key (estudianteIdiomaId) references hEstudianteIdioma(id)
);

create table dEstudianteIdiomaCarrera (
    estudianteIdiomaId int not null,
    carreraId int not null,
    primary key (carreraId, estudianteIdiomaId),
    foreign key (carreraId) references dCarrera(id),
    foreign key (estudianteIdiomaId) references hEstudianteIdioma(id)
);

-- hechoCarrera o cúal otro 