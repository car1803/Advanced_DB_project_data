import subprocess
import time

def execute_command(service, command, port):
    subprocess.run(["docker-compose", "exec", service, "mongosh", f'--port={port}', "--eval", command])

def main():
    print("configundo configsvr ","-" * 40)
    execute_command("configsvr", 'rs.initiate({"_id": "rs-config-server", "configsvr": true, "members": [{"_id": 0, "host": "configsvr:27017"}]})', 27017)

    print("configurando shard1 ","-" * 40)
    execute_command("shard1a", 'rs.initiate({"_id": "shard1", "members": [{"_id": 0, "host": "shard1a:27018"}, {"_id": 1, "host": "shard1b:27018"}]})', 27018)
    execute_command("shard1b", 'rs.initiate({"_id": "shard1", "members": [{"_id": 0, "host": "shard1a:27018"}, {"_id": 1, "host": "shard1b:27018"}]})', 27018)

    print("configurando mongos ","-" * 40)
    execute_command("mongos", 'sh.addShard("shard1/shard1a:27018")', 27017)
    execute_command("mongos", 'sh.addShard("shard1/shard1b:27018")', 27017)

if __name__ == "__main__":
    print("Iniciando docker-compose...")
    subprocess.run(["docker-compose", "up", "-d"])

    print("Esperando 20 segundos para iniciar os serviços...")
    time.sleep(20)
    main()
