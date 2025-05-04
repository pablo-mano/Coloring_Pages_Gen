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

// /generate endpoint
const { generateColoringPages } = require('./generate');

app.post('/generate', async (req, res) => {
  const { theme, count } = req.body;
  if (!theme) {
    return res.status(400).json({ error: 'Missing theme in request body' });
  }
  try {
    const { stdout, outputDir } = await generateColoringPages(theme, count || 1);
    res.json({ success: true, outputDir, log: stdout });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

// Placeholder for future endpoints: /auth, /payment, /download

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
