from pymongo import MongoClient

# Conexión a la base de datos MongoDB
client = MongoClient('localhost', 27017)
db = client['egresados']
collection = db['hregistroempresa']

# Eliminar colecciones existentes
db['empresa_por_tipo'].drop()
db['promedio_gasto_salarios_por_sector'].drop()
db['nombre_empresas_mas_frecuente'].drop()
db['carreras_mas_comunes_en_empresas'].drop()

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

# Agregación 4: Carreras más comunes en las empresas
pipeline_4 = [
  { "$unwind": "$dempresacarreras" }, # Descomponer cada carrera en un documento separado
  {
    "$group": {
      "_id": {
        "nombre_carrera": "$dempresacarreras.nombre",
        "tipo_carrera": "$dempresacarreras.nombretipocarrera",
        "facultad": "$dempresacarreras.nombrefacultad",
      },
      "count": { "$sum": 1 }
    } # Agrupar por nombre, tipo de carrera y departamento
  },
  {
    "$project": {
      "nombre": {"$concat" : [ "$_id.tipo_carrera", " - ", "$_id.nombre_carrera", " - ", "$_id.facultad"]}, # Crear un id único para cada carrera
      "tipo_carrera": "$_id.tipo_carrera",
      "nombre_carrera": "$_id.nombre_carrera",
      "facultad": "$_id.facultad",
      "count": 1,
      "_id": 0  # Esto elimina el campo _id
    }
  },
  {
    "$sort": { "count": -1 } # Ordenar por frecuencia descendente
  },
  {
    "$out": "carreras_mas_comunes_en_empresas"
  }
]
result_4 = collection.aggregate(pipeline_4)

# Cerrar conexión a la base de datos
client.close()