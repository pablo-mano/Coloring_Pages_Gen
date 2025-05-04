import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import { AppBar, Toolbar, Button, IconButton, Typography, Box, Container } from "@mui/material";
import PaletteIcon from '@mui/icons-material/Palette';
import Home from "./pages/Home";
import Generator from "./pages/Generator";
import Payment from "./pages/Payment";
import Dashboard from "./pages/Dashboard";
import Auth from "./pages/Auth";

import React, { useState } from "react";
import { TextField } from "@mui/material";

function App() {
  const [authenticated, setAuthenticated] = useState(false);
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const DEMO_PASSWORD = "test123";

  const handlePasswordSubmit = (e) => {
    e.preventDefault();
    if (password === DEMO_PASSWORD) {
      setAuthenticated(true);
      setError("");
    } else {
      setError("Incorrect password. Please try again.");
    }
  };

  if (!authenticated) {
    return (
      <Box sx={{ minHeight: "100vh", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", bgcolor: "#f7cac9" }}>
        <Box sx={{ p: 4, bgcolor: "white", borderRadius: 3, boxShadow: 3, minWidth: 320 }}>
          <Typography variant="h5" sx={{ mb: 2, fontWeight: 700 }}>Demo Access</Typography>
          <form onSubmit={handlePasswordSubmit}>
            <TextField
              type="password"
              label="Enter password"
              variant="outlined"
              value={password}
              onChange={e => setPassword(e.target.value)}
              fullWidth
              sx={{ mb: 2 }}
              autoFocus
            />
            {error && <Typography color="error" sx={{ mb: 1 }}>{error}</Typography>}
            <Button type="submit" variant="contained" color="primary" fullWidth>Access Demo</Button>
          </form>
        </Box>
      </Box>
    );
  }

  return (
    <Router>
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
            <IconButton edge="start" color="primary" aria-label="logo" sx={{ mr: 1 }} component={Link} to="/">
              <PaletteIcon fontSize="large" />
            </IconButton>
            <Typography variant="h5" sx={{ flexGrow: 1, fontWeight: 700, color: "#222" }}>
              Coloring Page Generator
            </Typography>
            <Button color="primary" component={Link} to="/" sx={{ mx: 1, fontWeight: 500 }}>
              Home
            </Button>
            <Button color="primary" component={Link} to="/generator" sx={{ mx: 1, fontWeight: 500 }}>
              Generator
            </Button>
            <Button color="primary" component={Link} to="/dashboard" sx={{ mx: 1, fontWeight: 500 }}>
              Dashboard
            </Button>
            <Button color="primary" component={Link} to="/payment" sx={{ mx: 1, fontWeight: 500 }}>
              Payment
            </Button>
            <Button variant="outlined" color="primary" component={Link} to="/auth" sx={{ fontWeight: 500, borderRadius: 2, px: 3, bgcolor: "#fff", ml: 2 }}>
              Login
            </Button>
          </Toolbar>
        </AppBar>
        <Container maxWidth="md" sx={{ flex: 1, display: "flex", alignItems: "center", justifyContent: "center" }}>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/generator" element={<Generator />} />
            <Route path="/payment" element={<Payment />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/auth" element={<Auth />} />
          </Routes>
        </Container>
        <Box sx={{ textAlign: "center", py: 2, bgcolor: "transparent" }}>
          <Typography variant="body2" sx={{ color: "#999", fontWeight: 400, letterSpacing: 1 }}>
            © {new Date().getFullYear()} Coloring Page Generator
          </Typography>
        </Box>
      </Box>
    </Router>
  );
}

export default App;
