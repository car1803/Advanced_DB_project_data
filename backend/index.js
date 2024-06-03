const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 5000;
app.use(cors());

// Conexión a MongoDB
mongoose.connect('mongodb://localhost:27017/egresados', {
  useNewUrlParser: true,
  useUnifiedTopology: true,
})
.then(async () => {
  console.log('Connected to MongoDB');
  
  // Obtener e imprimir nombres de las colecciones
  try {
    const db = mongoose.connection.db;
    const collections = await db.listCollections().toArray();
    const collectionNames = collections.map(col => col.name);
    console.log('Collections:', collectionNames);
  } catch (err) {
    console.error('Error retrieving collections:', err.message);
  }
  
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
    const validCollections = ['hregistrotrabajo', 'hregistroempresa', 'hregistroestudioidioma'];
    
    if (!validCollections.includes(collectionName)) {
      return res.status(400).send('Invalid collection name');
    }
    
    try {
      const db = mongoose.connection.db;
      const collection = db.collection(collectionName);
      const documents = await collection.find({}).limit(5).toArray();
      res.json(documents);
    } catch (err) {
      res.status(500).send('Error retrieving documents: ' + err.message);
    }
  });

  // Iniciar el servidor solo después de la conexión exitosa a MongoDB
  app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
  });
})
.catch(err => {
  console.error('Could not connect to MongoDB:', err);
  process.exit(1);  // Salir del proceso si no se puede conectar a MongoDB
});
