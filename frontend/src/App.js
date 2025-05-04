import React, { useState } from "react";
import { Box, Typography, TextField, Button, CircularProgress, AppBar, Toolbar, Container, IconButton } from "@mui/material";
import PaletteIcon from '@mui/icons-material/Palette';

function App() {
  const [prompt, setPrompt] = useState("");
  const [loading, setLoading] = useState(false);
  const [imageUrl, setImageUrl] = useState(null);
  const [error, setError] = useState("");

  const handleGenerate = () => {
    setLoading(true);
    setError("");
    setImageUrl(null);
    setTimeout(() => {
      setLoading(false);
      setImageUrl("https://placehold.co/400x400?text=Coloring+Page");
    }, 2000);
  };

  return (
    <Box
      sx={{
        minHeight: "100vh",
        width: "100vw",
        bgcolor: "linear-gradient(135deg, #f7cac9 0%, #92a8d1 100%)",
        background: "linear-gradient(135deg, #f7cac9 0%, #92a8d1 100%)",
        display: "flex",
        flexDirection: "column",
      }}
    >
      <AppBar position="static" elevation={0} sx={{ bgcolor: "rgba(255,255,255,0.75)", backdropFilter: "blur(8px)", boxShadow: "0 2px 16px 0 rgba(0,0,0,0.03)" }}>
        <Toolbar>
          <IconButton edge="start" color="primary" aria-label="logo" sx={{ mr: 1 }}>
            <PaletteIcon fontSize="large" />
          </IconButton>
          <Typography variant="h5" sx={{ flexGrow: 1, fontWeight: 700, color: "#222" }}>
            Coloring Page Generator
          </Typography>
          <Button variant="outlined" color="primary" sx={{ fontWeight: 500, borderRadius: 2, px: 3, bgcolor: "#fff" }}>
            Login
          </Button>
        </Toolbar>
      </AppBar>
      <Container maxWidth="sm" sx={{ flex: 1, display: "flex", alignItems: "center", justifyContent: "center" }}>
        <Box
          sx={{
            width: "100%",
            mt: 8,
            mb: 8,
            p: { xs: 3, sm: 5 },
            borderRadius: 6,
            boxShadow: "0 8px 32px 0 rgba(31, 38, 135, 0.15)",
            background: "rgba(255,255,255,0.65)",
            backdropFilter: "blur(12px)",
            border: "1px solid rgba(255,255,255,0.35)",
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
          }}
        >
          <Typography variant="h4" fontWeight={700} gutterBottom sx={{ letterSpacing: 1, color: "#4a4a4a" }}>
            Create Your Coloring Page
          </Typography>
          <Typography variant="subtitle1" sx={{ mb: 3, color: "#6b6b6b" }}>
            Describe what you want to see as a coloring page and generate a unique printable!
          </Typography>
          <TextField
            fullWidth
            label="e.g. 'A cat in a garden'"
            variant="filled"
            value={prompt}
            onChange={e => setPrompt(e.target.value)}
            sx={{ mb: 3, bgcolor: "rgba(255,255,255,0.85)", borderRadius: 2 }}
            InputProps={{ style: { fontSize: 18, padding: 8 } }}
            InputLabelProps={{ style: { fontSize: 16 } }}
          />
          <Button
            variant="contained"
            color="primary"
            disabled={!prompt || loading}
            onClick={handleGenerate}
            sx={{
              mb: 2,
              fontWeight: 600,
              fontSize: 18,
              borderRadius: 3,
              px: 5,
              py: 1.5,
              boxShadow: "0 2px 8px 0 rgba(31, 38, 135, 0.1)",
              background: "linear-gradient(90deg,#92a8d1 0%,#f7cac9 100%)",
              color: "#fff",
              transition: "background 0.3s",
              '&:hover': {
                background: "linear-gradient(90deg,#f7cac9 0%,#92a8d1 100%)",
              },
            }}
            fullWidth
            size="large"
          >
            {loading ? <CircularProgress size={24} color="inherit" /> : "Generate"}
          </Button>
          {error && (
            <Typography color="error" sx={{ mt: 2 }}>{error}</Typography>
          )}
          {imageUrl && (
            <Box sx={{ mt: 4, textAlign: "center", width: "100%" }}>
              <Box
                sx={{
                  display: "inline-block",
                  borderRadius: 5,
                  boxShadow: "0 4px 24px 0 rgba(31, 38, 135, 0.12)",
                  overflow: "hidden",
                  border: "2px solid #fff",
                  background: "#fafafa",
                }}
              >
                <img
                  src={imageUrl}
                  alt="Coloring Preview"
                  style={{ maxWidth: 340, width: "100%", display: "block" }}
                />
              </Box>
              <Typography variant="subtitle1" sx={{ mt: 2, color: "#666" }}>
                (Preview – Payment required to download)
              </Typography>
              <Button variant="contained" color="secondary" sx={{ mt: 2, fontWeight: 600, borderRadius: 2 }} disabled>
                Pay & Download
              </Button>
            </Box>
          )}
        </Box>
      </Container>
      <Box sx={{ textAlign: "center", py: 2, bgcolor: "transparent" }}>
        <Typography variant="body2" sx={{ color: "#999", fontWeight: 400, letterSpacing: 1 }}>
          © {new Date().getFullYear()} Coloring Page Generator
        </Typography>
      </Box>
    </Box>
  );
}

export default App;
