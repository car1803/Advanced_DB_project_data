from src.datos.postgresql.modeloRelacional import execute_script, create_schema, drop_schema, set_schema
from src.datos.postgresql.data import populate_tables
from src.connectors.postgresql.connection import connection

# Crear un objeto MetaData con el esquema especificado
esquemarelacional = "esquemaRelacional"
nombrearchivorelacional = "modeloRelacional"

drop_schema(esquemarelacional)
create_schema(esquemarelacional)
set_schema(esquemarelacional)
execute_script(nombrearchivorelacional)
populate_tables(100001, 10000)  # Siempre debe ser +1 de los que se quieren insertar

connection.close()