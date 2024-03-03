from src.datos.modeloRelacional import execute_script, execute_script_by_steps, create_schema, drop_schema, set_schema
from src.connectors.connection import connection

esquemadimesional = "esquemaDimensional"
nombremodelo = "modeloDimensional"
etl = "etl"

drop_schema(esquemadimesional)
create_schema(esquemadimesional)
set_schema(esquemadimesional)
execute_script(nombremodelo)
set_schema("public")
execute_script_by_steps(etl)

connection.close()