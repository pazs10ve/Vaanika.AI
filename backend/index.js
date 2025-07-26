const express = require('express');
const app = express();
const bodyParser = require('body-parser');
const cors = require('cors');
const AuthRouter = require('./Routes/AuthRouter');
const ProductRouter = require('./Routes/ProductRouter');
const SessionRouter = require('./Routes/SessionRouter');
const GenerateRouter = require('./Routes/GenerateRouter');

require('dotenv').config();
require('./Models/db');
const PORT = process.env.PORT || 8080;

app.get('/ping', (req, res) => {
    res.send('PONG');
});

app.use(bodyParser.json());
app.use(cors());
app.use('/auth', AuthRouter);
app.use('/products', ProductRouter);
app.use('/api/sessions', SessionRouter);
app.use('/api/generate', GenerateRouter);


app.listen(PORT, () => {
    console.log(`Server is running on ${PORT}`)
})