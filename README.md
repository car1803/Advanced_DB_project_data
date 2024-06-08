
*instalar estas dependencias*

```pip install faker ```
```pip install psycopg2-binary```
```pip install pymongo```
```pip install python-dotenv```


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

## Para montar todos los contenedores de docker NUEVO

```
cd .\docker\
python .\start-system.py
```

## Para montar todos los contenedores de docker (Método viejo)

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

### Crear varios chunks

_Nota: por defecto se está haciendo sharding con respecto a un id autogenerado en cada una de las colecciones._

Los comandos de esta sección requieren que haga primero _**use egresados**_

Puede hacer manualmente la división de los chunks de mongo db con el siguiente comando

```
sh.splitFind("egresados.<nombre_coleccion>",{id: <un_id_dentro_del_shard>})
```
Este comando hará un split en 2 automáticamente en el chunk que contenga el id _**<un_id_dentro_del_shard>**_

Para consultar el proceso de particion puede hacer:

```
db.<nombre_coleccion>.getShardDistribution()
```

### Ejecutar los mapreducers
Ingresar a la carpeta de cada colección de hechos en src/datos/mapreducers/x y ejecutar 
```
python mapreducers.py
```
Verificar en mongo compass las colecciones creadas.

otra forma es en la ruta base del proyecto ejecutar el comando:

```
python runallmapreducers.py
```

### Metabase
Ingresar a localhost:3300, loguearse y conectar la base de datos mongo (mongodb://docker-mongos-1:27017/egresados)

### Bajar los contenedores
```
cd .\docker\
docker-compose.exe down
```

## BACKEND

1. Ejecuta el siguiente comando para instalar las dependencias:
    ```bash
    cd backend
    npm install
    ```
2. Inicia el servidor con el siguiente comando:
    ```bash
    npm run server
    ```

## FRONTEND
primero debes instalar [Node.js](https://nodejs.org/en/blog/release/v18.20.2).
1. Ejecuta el siguiente comando para instalar las dependencias:
    ```bash
    cd frontend
    npm install
    ```
2. Inicia el servidor de desarrollo con el comando:
    ```bash
    npm start
    ```

Para obtener más información, consulta el archivo README dentro de la carpeta `frontend`.

# Ejecutar todo

Se incluye un archivo _package.json_ con el que se pueden ejecutar todos los componentes de un solo comando, para ello en la ruta base del proyecto ejecute:

```bash
npm i
npm run start
```

Al detener el script se detendran las instancias de node pero los contenedores de docker no, para detener los contenedores de docker ejecutar ```npm run stop-ri-only``` o ```npm run stop-all```


---
Ejecuta ambos componentes de manera local. Una vez ejecutado, el componente de back-end debería mostrar un mensaje de conexión exitosa a la base de datos de MongoDB, seguido de una lista de las colecciones presentes en la misma. Por otro lado, el componente de front-end mostrará un mensaje de éxito, acompañado de un enlace que te llevará a la página principal. En esta página principal, encontrarás un buscador donde podrás ingresar los valores 'trabajo', 'empresa' o 'idioma', dependiendo de la colección de datos que desees visualizar.