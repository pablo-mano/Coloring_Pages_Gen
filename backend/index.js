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
  
  // Input validation
  if (!theme || typeof theme !== 'string') {
    return res.status(400).json({ error: 'Missing or invalid theme in request body' });
  }
  
  if (theme.length > 100) {
    return res.status(400).json({ error: 'Theme must be less than 100 characters' });
  }
  
  // Sanitize theme to prevent command injection
  const sanitizedTheme = theme.replace(/[;&|`$<>]/g, '');
  
  if (count && (!Number.isInteger(count) || count < 1 || count > 10)) {
    return res.status(400).json({ error: 'Count must be an integer between 1 and 10' });
  }
  
  try {
    const { stdout, outputDir } = await generateColoringPages(sanitizedTheme, count || 1);
    res.json({ success: true, outputDir, log: stdout });
  } catch (err) {
    console.error('Generation error:', err);
    res.status(500).json({ success: false, error: 'Internal server error' });
  }
});

// Placeholder for future endpoints: /auth, /payment, /download

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
