require('dotenv').config();
const express = require('express');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 5000;

app.use(cors());
app.use(express.json());

// Health check endpoint
app.get('/', (req, res) => {
  res.json({ status: 'Backend API running!' });
});

// Placeholder for future endpoints: /auth, /generate, /payment, /download

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
