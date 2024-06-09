const express = require('express');
const cors = require('cors');
const mongoose = require('./database/mongocontroller');

const app = express();
const PORT = process.env.PORT || 5000;
app.use(cors());


console.log('Connected to MongoDB');

// Obtener e imprimir nombres de las colecciones

app.get('/getCollections', async (req, res) => {
  try {
    const db = mongoose.connection.db;
    const collections = await db.listCollections().toArray();
    const collectionNames = collections.map(col => col.name);
    res.json(collectionNames);
  } catch (err) {
    console.error('Error retrieving collections:', err.message);
    res.status(500).send('Error retrieving collections: ' + err.message);
  }
});

// Definir ruta para obtener nombres de las colecciones
app.get('/', async (req, res) => {
  try {
    const db = mongoose.connection.db;
    const collections = await db.listCollections().toArray();
    res.json(collections.map(col => col.name));
  } catch (err) {
    res.status(500).send('Error retrieving collections: ' + err.message);
  }
});

app.get('/:collectionName', async (req, res) => {
  const { collectionName } = req.params;
  const { query } = req.query;
  const db = mongoose.connection.db;
  const validCollections = await db.listCollections().toArray();
  const collectionNames = validCollections.map(col => col.name);
  if (!collectionNames.includes(collectionName)) {
    return res.status(400).send('Invalid collection name');
  }
  try {
    const collection = db.collection(collectionName);
    let documents = [];
    const start = process.hrtime();
    if (collectionName.startsWith('h')) {
      if (query) {
        documents = await collection.find(
          { $text: { $search: query } },
          { projection: { _id: 0, score: { $meta: "textScore" } } }
        ).sort({ score: { $meta: "textScore" } }).limit(100).toArray();
        if (documents.length === 0) {
          const regexQuery = new RegExp(query, 'i');
          documents = await collection.find(
            {
              $or: [
                { "cargo": regexQuery },
                { "nombre": regexQuery },
                { "descripcion": regexQuery },
                { "destudiante.nombre": regexQuery },
                { "destudiante.documento": regexQuery },
                { "dempresa.descripcion": regexQuery },
                { "dempresa.nombre": regexQuery },
                { "dtrabajoestudiantecarreras.nombrefacultad": regexQuery }, 
                { "destudianteidiomacarreras.nombrefacultad": regexQuery }, 
                { "dempresacarreras.nombrefacultad": regexQuery }, 
                { "destudianteidiomacarreras.nombresede": regexQuery }, 
                { "dempresacarreras.nombresede": regexQuery }, 
              ]
            },
            { projection: { _id: 0 } }
          ).limit(100).toArray();
        }
      } else {
        documents = await collection.find({}, { projection: { _id: 0 } }).limit(100).toArray();
      }
    } else {
      documents = await collection.find({}).limit(100).toArray();
    }
    const [seconds, nanoseconds] = process.hrtime(start);
    const queryTime = (seconds * 1000 + nanoseconds / 1e6).toFixed(3); // Convert to milliseconds and round to 3 decimal places
    res.json({ queryTime, documents });
  } catch (err) {
    res.status(500).send('Error retrieving documents: ' + err.message);
  }
});


// Iniciar el servidor solo después de la conexión exitosa a MongoDB
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
