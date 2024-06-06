const mongoose = require('mongoose');

mongoose.connect('mongodb://localhost:27017/egresados', {
    useNewUrlParser: true,
    useUnifiedTopology: true,
});

module.exports = mongoose;