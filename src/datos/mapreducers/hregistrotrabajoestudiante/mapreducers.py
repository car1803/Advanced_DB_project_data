from pymongo import MongoClient
from datetime import datetime

# Conexión a la base de datos MongoDB
client = MongoClient('localhost', 27017)
db = client['egresados']
collection = db['hregistrotrabajo']

# Eliminar colecciones existentes
db['salario_promedio_por_sector'].drop()
db['cantidad_personas_por_genero_y_sector'].drop()
db['palabras_mas_comunes_en_cargos'].drop()
db['estudiantes_por_genero'].drop()
db['salario_promedio_por_cargo'].drop()
db['edad_promedio_egresados'].drop()
db['estudiantes_por_pais'].drop()
db['salario_promedio_por_pais'].drop()
db['salario_promedio_por_genero'].drop()

# Agregación 1: Calcular el salario promedio por sector
pipeline_1 = [
    {"$group": {"_id": "$dempresa.nombresector", "salario_promedio": {"$avg": "$salariopromedio"}}}, # Mapeo en el group, reduce en el avg
    {"$out": "salario_promedio_por_sector"}  # Guardar resultado en colección
]
result_1 = collection.aggregate(pipeline_1)

# Agregación 2: Contar la cantidad de personas por género y por sector
pipeline_2 = [
    {
        "$group": {
            "_id": {
                "sector": "$dempresa.nombresector",
                "genero": "$destudiante.genero"
            },
            "count": {"$sum": 1}
        }
    },
    {
        "$group": {
            "_id": "$_id.sector",
            "cantidad_mujeres": {
                "$sum": {
                    "$cond": [
                        {"$eq": ["$_id.genero", "F"]},
                        "$count",
                        0
                    ]
                }
            },
            "cantidad_hombres": {
                "$sum": {
                    "$cond": [
                        {"$eq": ["$_id.genero", "M"]},
                        "$count",
                        0
                    ]
                }
            }
        }
    },
    {"$out": "cantidad_personas_por_genero_y_sector"}
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

# Estudiantes, salario y edad promedio por genero
pipeline_4 = [
    {
        "$project": {
            "edad":{ "$divide" : [ {"$toLong" : { "$subtract": [datetime.now(),"$destudiante.fechanacimiento" ]}} ,  {"$toLong": "31536000000"}]},
            "destudiante.genero": 1,
            "salariopromedio": 1,
        }
    },
    {
        "$group": {
            "_id": "$destudiante.genero",
            "count": {"$sum": 1},
            "edad_promedio": { "$avg": "$edad"},
            "salario_promedio": { "$avg": "$salariopromedio"}
        }
    },
    {"$out": "estudiantes_por_genero"}
]
result_4 = collection.aggregate(pipeline_4)

# Salario promedio por cargos

pipeline_5 = [
  {
    "$group": {
      "_id": "$cargo",
      "salario_promedio": { "$avg": "$salariopromedio" }
    }
  },
    {
        "$out": "salario_promedio_por_cargo"
    }
]
result_5 = collection.aggregate(pipeline_5)

# Edad promedio de egresados 
pipeline_6 = [
    {
        "$project": {
            "edad":{ "$divide" : [ {"$toLong" : { "$subtract": [datetime.now(),"$destudiante.fechanacimiento" ]}} ,  {"$toLong": "31536000000"}]},
        }
    },
     {
    "$group": {
      "_id": 0,
      "edad_promedio": { "$avg": "$edad" }
        }
    },
    {
        "$out": "edad_promedio_egresados"
    }
]

result_6 = collection.aggregate(pipeline_6)


# Cantidad de estudiantes por pais

pipeline_7 = [
  {
    "$group": {
      "_id": "$destudiante.nombrepais",
      "count": { "$sum": 1 }
    }
  },
    {
        "$out": "estudiantes_por_pais"
    }
]

result_7 = collection.aggregate(pipeline_7)

# Promedio salario y edad por pais
pipeline_8 = [
  {
    "$project": {
        "salariopromedio": 1,
        "destudiante.nombrepais": 1,
        "edad":{ "$divide" : [ {"$toLong" : { "$subtract": [datetime.now(),"$destudiante.fechanacimiento" ]}} ,  {"$toLong": "31536000000"}]}
    }
  },
  {
    "$group": {
      "_id": "$destudiante.nombrepais",
      "salario_promedio": { "$avg": "$salariopromedio" },
      "edad_promedio": { "$avg": "$edad" }
    }
  },
  {
    "$sort": { "salario_promedio": -1 }
  },
    {
        "$out": "salario_promedio_por_pais"
    }
]
result_8 = collection.aggregate(pipeline_8)

#salarios por genero
pipeline_9 = [
    {
        "$group": {
            "_id": "$destudiante.genero",
            "salario_promedio": { "$avg": "$salariopromedio" }
        }
    },
    {
        "$out": "salario_promedio_por_genero"
    }
]
result_9 = collection.aggregate(pipeline_9)


# Cerrar conexión a la base de datos
client.close()
