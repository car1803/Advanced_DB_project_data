import subprocess
import time
import os
import sys


data_server_config = "configsvr-data"

def execute_command(service, command, port, fileDockerCompose):
    subprocess.run(["docker-compose","-f", fileDockerCompose, "exec", service, "mongosh", f'--port={port}', "--eval", command])

def main(fileDockerCompose):
    print("configundo configsvr ","-" * 40)
    execute_command("configsvr", 'rs.initiate({"_id": "rs-config-server", "configsvr": true, "members": [{"_id": 0, "host": "configsvr:27017"}]})', 27017,fileDockerCompose)

    print("configurando shard1 ","-" * 40)
    execute_command("shard1a", 'rs.initiate({"_id": "shard1", "members": [{"_id": 0, "host": "shard1a:27018"}, {"_id": 1, "host": "shard1b:27018"}]})', 27018,fileDockerCompose)
    execute_command("shard1b", 'rs.initiate({"_id": "shard1", "members": [{"_id": 0, "host": "shard1a:27018"}, {"_id": 1, "host": "shard1b:27018"}]})', 27018,fileDockerCompose)
    execute_command("shard2a", 'rs.initiate({"_id": "shard2", "members": [{"_id": 0, "host": "shard2a:27018"}, {"_id": 1, "host": "shard2b:27018"}]})', 27018,fileDockerCompose)
    execute_command("shard2b", 'rs.initiate({"_id": "shard2", "members": [{"_id": 0, "host": "shard2a:27018"}, {"_id": 1, "host": "shard2b:27018"}]})', 27018,fileDockerCompose)

    print("configurando mongos ","-" * 40)
    execute_command("mongos", 'sh.addShard("shard1/shard1a:27018")', 27017,fileDockerCompose)
    execute_command("mongos", 'sh.addShard("shard1/shard1b:27018")', 27017,fileDockerCompose)
    execute_command("mongos", 'sh.addShard("shard2/shard2a:27018")', 27017,fileDockerCompose)
    execute_command("mongos", 'sh.addShard("shard2/shard2b:27018")', 27017,fileDockerCompose)

    print("configurando colecciones ","-" * 40)
    execute_command("mongos", 'sh.enableSharding("egresados")', 27017,fileDockerCompose)
    execute_command("mongos", 'sh.shardCollection("egresados.hregistrotrabajo", {"id": 1})', 27017,fileDockerCompose)
    execute_command("mongos", 'sh.shardCollection("egresados.hregistroestudioidioma", {"id": 1})', 27017,fileDockerCompose)
    execute_command("mongos", 'sh.shardCollection("egresados.hregistroempresa", {"id": 1})', 27017,fileDockerCompose)

    print("configurando indices de texto ","-" * 40)
    execute_command("mongos", 'db = connect("localhost/egresados"); db.hregistrotrabajo.createIndex({"cargo": "text", "destudiante.nombre": "text", "dempresa.descripcion":"text", "dempresa.nombre":"text", "dtrabajoestudiantecarreras.nombrefacultad":"text"},{ default_language: "english" })', 27017,fileDockerCompose)
    execute_command("mongos", 'db = connect("localhost/egresados"); db.hregistroestudioidioma.createIndex({"destudiante.nombre" : "text", "destudianteidiomacarreras.nombrefacultad":"text", "destudianteidiomacarreras.nombresede":"text", "destudiante.documento":"text"}, { default_language: "english" })', 27017,fileDockerCompose)
    execute_command("mongos", 'db = connect("localhost/egresados"); db.hregistroempresa.createIndex({"nombre": "text", "descripcion": "text", "dempresacarreras.nombrefacultad":"text", "dempresacarreras.nombresede":"text"}, { default_language: "english" })', 27017,fileDockerCompose)


if __name__ == "__main__":

    fileDockerCompose = "docker-compose.yaml"

    if len(sys.argv) >= 2:
        param1 = sys.argv[1]
        if param1 != None:
            fileDockerCompose = param1
    
    print(f"Usando archivo de docker-compose: {fileDockerCompose}")
    ruta_actual = os.getcwd()
    ruta_completa = os.path.join(ruta_actual, data_server_config)
    if os.path.exists(ruta_completa) and os.path.isdir(ruta_completa):
        print("Iniciando docker-compose...")
        subprocess.run(["docker-compose","-f", fileDockerCompose, "up", "-d"])
        print(f"Ya se ha creado la carpeta de datos de configsrv no es necesario correr la migración.")
    else:
        print("Iniciando docker-compose...")
        subprocess.run(["docker-compose","-f", fileDockerCompose, "up", "-d"])
        print("Esperando 20 segundos para iniciar los servicios...")
        time.sleep(20)
        main(fileDockerCompose)