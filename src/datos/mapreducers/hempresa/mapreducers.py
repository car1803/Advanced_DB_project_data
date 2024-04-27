from pymongo import MongoClient

# Conexión a la base de datos MongoDB
client = MongoClient('localhost', 27017)
db = client['egresados']
collection = db['hregistroempresa']

# Eliminar colecciones existentes
db['empresa_por_tipo'].drop()
db['promedio_gasto_salarios_por_sector'].drop()
db['nombre_empresas_mas_frecuente'].drop()

# Agregación 1: Contar la Cantidad de Empresas por Tipo
pipeline_1 = [
    {"$group": {"_id": "$dtipoempresa.nombre", "count": {"$sum": 1}}}, # Mapeo en el group, reduce en el sum
    {"$out": "empresa_por_tipo"}  # Guardar resultado en colección
]
result_1 = collection.aggregate(pipeline_1)

# Agregación 2: Calcular el Promedio de Gastos en Salarios por Sector
pipeline_2 = [
    {"$group": {"_id": "$dsector.nombre", "avg_gasto_salarios": {"$avg": "$gastoensalariostotal"}}}, # Mapeo en el group, reduce en el avg
    {"$out": "promedio_gasto_salarios_por_sector"} # Guardar resultado en colección
]
result_2 = collection.aggregate(pipeline_2)

# Agregación 3: Nombre de empresas más frecuentes
pipeline_3 = [
    {"$project": {"_id": 0, "words": {"$split": ["$nombre", " "]}}},  # Dividir el nombre en palabras
    {"$unwind": "$words"},  # Descomponer cada palabra en un documento separado
    {"$group": {"_id": "$words", "count": {"$sum": 1}}},  # Contar la frecuencia de cada palabra, mapeo en el group, reduce en el sum
    {"$sort": {"count": -1}},  # Ordenar por frecuencia descendente
    {"$out": "nombre_empresas_mas_frecuente"}  # Guardar resultado en colección
]
result_3 = collection.aggregate(pipeline_3)

# Cerrar conexión a la base de datos
client.close()