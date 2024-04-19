
*instalar estas dependencias*

```pip install faker ```
```pip install psycopg2-binary```

o simplemente

```pip install -r requirements.txt ```

*para trabajar con virtualenv*

```pip install virtualenv ```
```virtualenv egresadosenv ```
```.\egresadosenv\Scripts\Activate ```

*En caso de que el ultimo codigo falle:*

```set "VIRTUAL_ENV=.\egresadosenv" ```
```set "PATH=%VIRTUAL_ENV%\Scripts;%PATH%" ```

# Ejecución:

Ejecutar los archivos crearEsquemaRelacionalYpoblarlo y pycrearEsquemaDimensionalyPoblarlo.py, estos archivos generan el esquema relacional, el dimensional y generan los datos ficticios en el relacional y ejecutan el etl al relacional.

```
python .\crearEsquemaRelacionalYpoblarlo.py
python .\crearEsquemaDimensionalyPoblarlo.py
```

Para configurar la base de datos, el esquema y demás, utilizar un archivo .env con la siguiente estructura y ponerlo en la ruta base del proyecto.

```
POSTGRES_HOST=localhost
POSTGRES_DATABASE=egresados
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin
```
### Para montar postgres en docker.

```
docker-compose -f .\postgres\docker-compose.yaml up -d
```

segun las credenciales que hemos definido en el docker-compose.yaml hacemos la coneccion con dbeaver

### Para montar mongo en docker

```
docker-compose -f .\mongoDB\docker-compose.yaml up -d
```

luego para añadir los shards al servidor de configuracion ejecute __sin eso no sirve__.

```
cd .\mongoDB\
python3 .\configurar_sharding.py
```
__Nota__: hay que configurar el sharding una vez poblada o antes de poblar la db.
