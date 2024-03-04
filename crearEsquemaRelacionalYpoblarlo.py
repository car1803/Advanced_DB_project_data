from src.datos.modeloRelacional import execute_script, create_schema, drop_schema, set_schema
from src.datos.data import populate_tables
from src.connectors.connection import connection

# Crear un objeto MetaData con el esquema especificado
esquemarelacional = "esquemaRelacional"
nombrearchivorelacional = "modeloRelacional"

drop_schema(esquemarelacional)
create_schema(esquemarelacional)
set_schema(esquemarelacional)
execute_script(nombrearchivorelacional)
populate_tables(100001, 10000)  # Se preuba con menos datos para salir de errores rápido

connection.close()