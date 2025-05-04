import React from "react";
import { Typography, Box, Button } from "@mui/material";
import { Link } from "react-router-dom";

const Home = () => (
  <Box sx={{ textAlign: "center", mt: 10 }}>
    <Typography variant="h3" fontWeight={700} color="#333" gutterBottom>
      Welcome to the Coloring Page Generator!
    </Typography>
    <Typography variant="h6" color="#666" sx={{ mb: 4 }}>
      Create, preview, and purchase custom coloring pages.
    </Typography>
    <Button
      variant="contained"
      color="primary"
      size="large"
      component={Link}
      to="/generator"
      sx={{
        px: 5,
        py: 2,
        fontWeight: 600,
        fontSize: 20,
        borderRadius: 3,
        boxShadow: "0 4px 18px 0 rgba(146,168,209,0.18)",
        background: "linear-gradient(90deg,#92a8d1 0%,#f7cac9 100%)",
        color: "#fff",
        mt: 3,
        '&:hover': {
          background: "linear-gradient(90deg,#f7cac9 0%,#92a8d1 100%)",
        },
      }}
    >
      Start Generating Now
    </Button>
  </Box>
);

export default Home;
