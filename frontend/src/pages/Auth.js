import React from "react";
import { Typography, Box, Button } from "@mui/material";

const Auth = () => (
  <Box sx={{ mt: 8, textAlign: "center" }}>
    <Typography variant="h4" fontWeight={600} gutterBottom>
      Login / Register
    </Typography>
    <Button variant="contained" color="primary" sx={{ mt: 2 }} disabled>
      Sign In
    </Button>
    <Button variant="outlined" color="primary" sx={{ mt: 2, ml: 2 }} disabled>
      Register
    </Button>
  </Box>
);

export default Auth;
