from src.datos.modeloRelacional import create_tables, create_schema, drop_schema
from src.datos.data import populate_tables
from src.connectors.connection import connection
from src.connectors.postgresqlcredenciales import schema

# Crear un objeto MetaData con el esquema especificado
drop_schema(schema)
create_schema(schema)
create_tables(schema)
populate_tables()

connection.close()