from src.datos.modeloRelacional import create_tables, create_schema, drop_schema, set_schema
from src.datos.data import populate_tables
from src.connectors.connection import connection

# Crear un objeto MetaData con el esquema especificado
esquemarelacional = "esquemaRelacional"
nombrearchivorelacional = "modeloRelacional"

#Esto está comentado por seguridad  :v
#drop_schema(esquemarelacional)
#create_schema(esquemarelacional)
#set_schema(esquemarelacional)
#create_tables(nombrearchivorelacional)
#populate_tables(100001, 1000) # TODO: incluir acá el esquema actualmente usa el que está en el archivo de credenciales


esquemadimesional = "esquemaDimensional"
nombrearchivodimensional = "modeloDimensional"

#drop_schema(esquemadimesional)
#create_schema(esquemadimesional)
#set_schema(esquemadimesional)
#create_tables(nombrearchivodimensional)
#TODO: implementar ETL para migrar datos del esquema relacional al esquema dimensional

connection.close()