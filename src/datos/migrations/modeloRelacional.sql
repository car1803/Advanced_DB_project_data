-- Modelo relacional

drop table if exists trabajoEstudianteSalario;
drop table if exists trabajoEstudiante;
drop table if exists empresa;
drop table if exists tipoEmpresa;
drop table if exists sector;
drop table if exists educacionExterna;
drop table if exists institucionExterna;
drop table if exists estudianteIdioma;
drop table if exists idiomaNivel;
drop table if exists idioma;
drop table if exists egresado;
drop table if exists carrera;
drop table if exists departamento;
drop table if exists facultad;
drop table if exists sede;
drop table if exists tipoCarrera;
drop table if exists estudiante;
drop table if exists tipoDocumento;
drop table if exists pais;

create table pais (
	id serial primary key, 
	nombre varchar(255) not null
);

create table tipoDocumento (
	id serial primary key, 
	nombre varchar(255) not null
);

create table estudiante (
    id serial primary key,
    nombre varchar(255) not null,
    correo varchar(255) not null,
	apellido varchar(255) not null,
    fechaNacimiento date not null,
    genero varchar(1) not null,
    documento varchar(255) not null,
    paisId int not null, 
    tipoDocumentoId int not null, 
    foreign key (paisId) references pais (id), 
    foreign key (tipoDocumentoId) references tipoDocumento (id)
);

create table tipoCarrera (
	id serial primary key, 
	nombre varchar(255) not null
);

create table sede (
	id serial primary key, 
	nombre varchar(255) not null
);

create table facultad (
	id serial primary key, 
	nombre varchar(255) not null, 
	sedeId int not null, 
	foreign key (sedeId) references sede(id)
);

create table departamento (
	id serial primary key, 
	nombre varchar(255) not null, 
	facultadId int not null, 
	foreign key (facultadId) references facultad(id)
);

create table carrera (
	id serial primary key,
	nombre varchar(255) not null, 
	tipoCarreraId int not null, 
	departamentoId int not null, 
	foreign key (tipoCarreraId) references tipoCarrera(id), 
	foreign key (departamentoId) references departamento(id)
);

create table egresado (
	id serial primary key,
	año int not null, 
	carreraId int not null, 
	estudianteId int not null, 
	foreign key (carreraId) references carrera (id), 
	foreign key (estudianteId) references estudiante (id)
); 

create table idioma (
	id serial primary key, 
	nombre varchar(255) not null
); 

create table idiomaNivel (
	id serial primary key, 
	nombre varchar(255) not null
); 

create table estudianteIdioma (
	id serial primary key, 
	idiomaId int not null, 
	idiomaNivelId int not null, 
	estudianteId int not null,
	foreign key (idiomaId) references idioma (id), 
	foreign key (idiomaNivelId) references idiomaNivel (id), 
	foreign key (estudianteId) references estudiante (id)
); 

create table institucionExterna (
	id serial primary key,
	nombre varchar(255) not null, 
	paisId int not null,
	foreign key (paisId) references pais (id)
); 

create table educacionExterna (
	id serial primary key,
	nombre varchar(255) not null, 
	año int not null, 
	institucionExternaId int not null, 
	estudianteId int not null, 
	tipoCarreraId int not null, 
	foreign key (institucionExternaId) references institucionExterna (id), 
	foreign key (estudianteId) references estudiante (id), 
	foreign key (tipoCarreraId) references tipoCarrera (id)
); 

create table sector(
	id serial primary key, 
	nombre varchar(255) not null
); 

create table tipoEmpresa (
	id serial primary key, 
	nombre varchar(255) not null
); 

create table empresa (
	id serial primary key,
	nombre varchar(255) not null, 
	correo varchar(255), 
	web varchar(255),  
	tipoEmpresaId int not null, 
	sectorId int not null, 
	foreign key (tipoEmpresaId) references tipoEmpresa (id), 
	foreign key (sectorId) references sector (id)
); 

create table trabajoEstudiante (
	id serial primary key,
	fechaInicio date not null, 
	fechaFin date, 
	orden int,
	cargo varchar(255) not null, 
	añosExperienciaPrevia int not null, 
	ofertaSie boolean not null,
	estudianteId int not null, 
	empresaId int not null, 
	foreign key (estudianteId) references estudiante (id), 
	foreign key (empresaId) references empresa (id)
); 

create table trabajoEstudianteSalario (
	id serial primary key,
	salario float not null,
	trabajoEstudianteId int not null, 
	foreign key (trabajoEstudianteId) references trabajoEstudiante (id)
); 
