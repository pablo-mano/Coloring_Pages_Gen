import React, { useState } from "react";
import { Box, Typography, TextField, Button, CircularProgress } from "@mui/material";

const Generator = () => {
  const [prompt, setPrompt] = useState("");
  const [loading, setLoading] = useState(false);
  const [imageUrl, setImageUrl] = useState(null);

  const handleGenerate = () => {
    setLoading(true);
    setTimeout(() => {
      setLoading(false);
      setImageUrl("https://placehold.co/400x400?text=Coloring+Page");
    }, 2000);
  };

  return (
    <Box sx={{ mt: 8, display: "flex", flexDirection: "column", alignItems: "center" }}>
      <Typography variant="h4" fontWeight={600} gutterBottom>
        Generate a Coloring Page
      </Typography>
      <TextField
        label="Describe your coloring page"
        variant="outlined"
        value={prompt}
        onChange={e => setPrompt(e.target.value)}
        sx={{ mb: 2, width: 400, maxWidth: "90%" }}
      />
      <Button variant="contained" color="primary" onClick={handleGenerate} disabled={loading || !prompt}>
        {loading ? <CircularProgress size={24} /> : "Generate"}
      </Button>
      {imageUrl && (
        <Box sx={{ mt: 4 }}>
          <img src={imageUrl} alt="Generated coloring page" style={{ maxWidth: 400, width: "100%" }} />
          <Typography variant="subtitle1" sx={{ mt: 2, color: "#666" }}>
            (Preview – Payment required to download)
          </Typography>
        </Box>
      )}
    </Box>
  );
};

export default Generator;
