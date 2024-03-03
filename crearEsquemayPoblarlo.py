from src.datos.modeloRelacional import create_tables, create_schema, drop_schema, set_schema
from src.datos.data import populate_tables
from src.connectors.connection import connection
from src.connectors.postgresqlcredenciales import schema
import sys
parametro = sys.argv[1]

# Crear un objeto MetaData con el esquema especificado
drop_schema(schema)
create_schema(schema)
set_schema(schema)
create_tables("modeloRelacional")

populate_tables(201, 100)

connection.close()