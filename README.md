
*instalar estas dependencias*

```pip install faker ```
```pip install psycopg2-binary```

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
MONGODB_URI=mongodb+srv://<client>:<pasword>@cluster0.t1opyro.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0
MONGODB_DATABASE=egresados
```

## Para montar todos los contenedores de docker

```
docker-compose -f .\docker\docker-compose.yaml up -d
```
Nota: solo es necesario ejecutar lo una vez

### Migrar postgres en docker.

Ejecutar los archivos crearEsquemaRelacionalYpoblarlo y pycrearEsquemaDimensionalyPoblarlo.py, estos archivos generan el esquema relacional, el dimensional y generan los datos ficticios en el relacional y ejecutan el etl al relacional.

```
python .\crearEsquemaRelacionalYpoblarlo.py
python .\crearEsquemaDimensionalyPoblarlo.py
```

segun las credenciales que hemos definido en el docker-compose.yaml hacemos la coneccion con dbeaver

### Para montar mongo en docker

Añadir los shards al servidor de configuracion ejecute __sin eso no sirve__.

```
cd .\docker\
python3 .\configurar_sharding.py
```
__Nota__: hay que configurar el sharding una vez poblada o antes de poblar la db.

### migrar datos a docker
es recomendable ejecutar primero el siguiente codigo, recordar tener el docker corriendo
```
python .\test_postgres-mongo_connection.py
```
ejecutar (aun no esta listo)
```
python .\etl_Mongo.py
```

### Migrar con MongoMR

Primero corra con docker el mongoMR