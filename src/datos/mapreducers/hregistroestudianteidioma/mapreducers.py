from pymongo import MongoClient

# Conexión a la base de datos MongoDB
client = MongoClient('localhost', 27017)
db = client['egresados']
collection = db['hregistroestudioidioma']

# Eliminar colecciones existentes
db['cantidad_estudiantes_por_idioma'].drop()
db['promedio_nivel_por_idioma'].drop()
db['niveles_idioma_mas_comunes'].drop()

# Agregación 1: Contar la cantidad de estudiantes por idioma
pipeline_1 = [
    {"$group": {"_id": "$didioma.nombre", "cantidad_estudiantes": {"$sum": 1}}}, # Map en el group, reduce en el sum
    {"$sort": {"cantidad_estudiantes": -1}},  # Ordenar por cantidad de estudiantes descendente
    {"$out": "cantidad_estudiantes_por_idioma"}  # Guardar resultado en colección
]
result_1 = collection.aggregate(pipeline_1)

# Agregación 2: Calcular el promedio de niveles de idioma por idioma
pipeline_2 = [
    # Asignar valores numéricos a los niveles de idioma
    {"$addFields": {
        "nivel_numerico": {
            "$switch": {
                "branches": [
                    {"case": {"$eq": ["$didiomanivel.nombre", "A1"]}, "then": 1},
                    {"case": {"$eq": ["$didiomanivel.nombre", "A2"]}, "then": 2},
                    {"case": {"$eq": ["$didiomanivel.nombre", "B1"]}, "then": 3},
                    {"case": {"$eq": ["$didiomanivel.nombre", "B2"]}, "then": 4},
                    {"case": {"$eq": ["$didiomanivel.nombre", "C1"]}, "then": 5},
                    {"case": {"$eq": ["$didiomanivel.nombre", "C2"]}, "then": 6}
                ],
                "default": 0 # Valor por defecto
            }
        }
    }},
    # Agrupar por idioma y calcular el promedio de los niveles numéricos
    {"$group": {"_id": "$didioma.nombre", "promedio_nivel_numerico": {"$avg": "$nivel_numerico"}}},
    # Redondear el promedio de niveles
    {"$addFields": {
        "promedio_nivel_redondeado": {"$round": ["$promedio_nivel_numerico", 0]}
    }},
    # Asignar valores numéricos a los niveles de idioma
    {"$addFields": {
        "promedio_nivel": {
            "$switch": {
                "branches": [
                    {"case": {"$eq": ["promedio_nivel_redondeado", 1]}, "then": "A1"},
                    {"case": {"$eq": ["$promedio_nivel_redondeado", 2]}, "then": "A2"},
                    {"case": {"$eq": ["$promedio_nivel_redondeado", 3]}, "then": "B1"},
                    {"case": {"$eq": ["$promedio_nivel_redondeado", 4]}, "then": "B2"},
                    {"case": {"$eq": ["$promedio_nivel_redondeado", 5]}, "then": "C1"},
                    {"case": {"$eq": ["$promedio_nivel_redondeado", 6]}, "then": "C2"}
                ],
                "default": "N/A" # Valor por defecto
            }
        }
    }},
    # Ordenar por promedio de nivel descendente
    {"$sort": {"promedio_nivel_numerico": -1}},
    # Guardar resultado en colección
    {"$out": "promedio_nivel_por_idioma"}
]
result_2 = collection.aggregate(pipeline_2)

# Agregación 3: Encontrar los niveles de idioma más comunes
pipeline_3 = [
    {"$group": {"_id": "$didiomanivel.nombre", "cantidad": {"$sum": 1}}}, # Map en el group, reduce en el sum
    {"$sort": {"cantidad": -1}},  # Ordenar por cantidad descendente
    {"$out": "niveles_idioma_mas_comunes"}  # Guardar resultado en colección
]
result_3 = collection.aggregate(pipeline_3)

# Cerrar conexión a la base de datos
client.close()
