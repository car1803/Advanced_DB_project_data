
*instalar estas dependencias*

```pip install faker ```
```pip install psycopg2-binary```
```pip install pymongo```


o simplemente

```pip install -r requirements.txt ```

*para trabajar con virtualenv*

```pip install virtualenv ```
```virtualenv egresadosenv ```
```.\egresadosenv\Scripts\Activate ```

# Ejecución:

Para configurar la base de datos, el esquema y demás, utilizar un archivo .env con la siguiente estructura y ponerlo en la ruta base del proyecto.

```
POSTGRES_HOST=localhost
POSTGRES_PORT=5433
POSTGRES_DATABASE=egresados
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin
```

## Para montar todos los contenedores de docker

```
docker-compose -f .\docker\docker-compose.yaml up -d
```
Nota: solo es necesario ejecutar lo una vez

Iniciar los contenedores

```
cd .\docker\
docker-compose.exe up -d
```

Ejecutar el siguiente comando cada vez que se apaguen y se prendan los contenedores, deben aparecer dos json para confirmar que este bien:

```
cd .\docker\
python3 .\configurar_sharding.py
```
__Nota__: hay que configurar el sharding una vez poblada o antes de poblar la db.

### Migrar postgres en docker.

Ejecutar los archivos crearEsquemaRelacionalYpoblarlo y pycrearEsquemaDimensionalyPoblarlo.py, estos archivos generan el esquema relacional, el dimensional y generan los datos ficticios en el relacional y ejecutan el etl al relacional.

```
python .\crearEsquemaRelacionalYpoblarlo.py
python .\crearEsquemaDimensionalyPoblarlo.py
```

segun las credenciales que hemos definido en el docker-compose.yaml hacemos la coneccion con dbeaver

### Migrar con MongoRM
- Posicionandonos en el contenedor docker, abrimos el contenedor mongoRM que esta corriendo en el puerto 8080
- Nos conectamos a una base de datos poniendo los valores
    1) type: postgreSQL
    2) host: postgres_db
    3) port: 5432
    4) database: egresados
    5) credenciales: admin
- Seleccionamos el esquemadimensional y todas las tablas
- Seleccionar Start with a recommended MongoDB schema y solo las tablas de hechos
- Seleccionamos Crear migration job y en la coneccion de destino, escoger la opcionde uri y poner mongodb://docker-mongos-1:27017/egresados
- Ahora en mongoDB compass nos conectamos al mongodb://localhost:27017
- (En caso tal de que ya tengamos el etl, importamos este de src/datos/migrations)

### Ejecutar los mapreducers
Ingresar a la carpeta de cada colección de hechos en src/datos/mapreducers/x y ejecutar 
```
python3 mapreducers.py
```
Verificar en mongo compass las colecciones creadas.

### Bajar los contenedores
```
cd .\docker\
docker-compose.exe down
```