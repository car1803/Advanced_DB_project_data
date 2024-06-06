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

// Ruta para obtener los primeros 5 documentos de una colección específica
app.get('/:collectionName', async (req, res) => {
  const { collectionName } = req.params;
  const db = mongoose.connection.db;
  const validCollections = await db.listCollections().toArray();
  const collectionNames = validCollections.map(col => col.name);

  if (!collectionNames.includes(collectionName)) {
    return res.status(400).send('Invalid collection name');
  }

  try {
    const db = mongoose.connection.db;
    const collection = db.collection(collectionName);
    var documents = {};

    //Verificar si la colección empieza por h
    if (collectionName.startsWith('h')) {
      documents = await collection.find({}, { projection: { _id: 0 } }).limit(100).toArray();
    } else {
      documents = await collection.find({}, {}).limit(100).toArray();
    }
    
    res.json(documents);
  } catch (err) {
    res.status(500).send('Error retrieving documents: ' + err.message);
  }
});

// Iniciar el servidor solo después de la conexión exitosa a MongoDB
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
