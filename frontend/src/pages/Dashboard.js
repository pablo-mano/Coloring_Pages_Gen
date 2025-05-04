import React from "react";
import { Typography, Box } from "@mui/material";

const Dashboard = () => (
  <Box sx={{ mt: 8, textAlign: "center" }}>
    <Typography variant="h4" fontWeight={600} gutterBottom>
      My Coloring Pages
    </Typography>
    <Typography variant="body1">
      (Login to view your generated and purchased coloring pages.)
    </Typography>
  </Box>
);

export default Dashboard;
