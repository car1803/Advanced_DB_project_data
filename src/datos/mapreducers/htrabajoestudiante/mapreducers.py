from pymongo import MongoClient

# Conexión a la base de datos MongoDB
client = MongoClient('localhost', 27017)
db = client['egresados']
collection = db['htrabajoestudiante']

# Eliminar colecciones existentes
db['salario_promedio_por_sector'].drop()
db['cantidad_personas_por_genero_y_sector'].drop()
db['palabras_mas_comunes_en_cargos'].drop()

# Agregación 1: Calcular el salario promedio por sector
pipeline_1 = [
    {"$group": {"_id": "$dempresa.nombresector", "salario_promedio": {"$avg": "$salariopromedio"}}}, # Mapeo en el group, reduce en el avg
    {"$out": "salario_promedio_por_sector"}  # Guardar resultado en colección
]
result_1 = collection.aggregate(pipeline_1)

# Agregación 2: Contar la cantidad de personas por género y por sector
pipeline_2 = [
    {"$group": {"_id": {"genero": "$destudiante.genero", "sector": "$dempresa.nombresector"}, "cantidad_personas": {"$sum": 1}}}, # Mapeo en el group, reduce en el sum
    {"$out": "cantidad_personas_por_genero_y_sector"}  # Guardar resultado en colección
]
result_2 = collection.aggregate(pipeline_2)

# Agregación 3: Encontrar las palabras más comunes en los cargos
pipeline_3 = [
    {"$project": {"_id": 0, "words": {"$split": ["$cargo", " "]}}},  # Dividir el cargo en palabras
    {"$unwind": "$words"},  # Descomponer cada palabra en un documento separado
    {"$group": {"_id": "$words", "count": {"$sum": 1}}},  # Contar la frecuencia de cada palabra
    {"$sort": {"count": -1}},  # Ordenar por frecuencia descendente
    {"$out": "palabras_mas_comunes_en_cargos"}  # Guardar resultado en colección
]
result_3 = collection.aggregate(pipeline_3)

# Cerrar conexión a la base de datos
client.close()
