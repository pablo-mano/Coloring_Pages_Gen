import React from "react";
import { Typography, Box, Button } from "@mui/material";

const Payment = () => (
  <Box sx={{ mt: 8, textAlign: "center" }}>
    <Typography variant="h4" fontWeight={600} gutterBottom>
      Payment / Checkout
    </Typography>
    <Typography variant="body1" sx={{ mb: 2 }}>
      (Stripe integration coming soon)
    </Typography>
    <Button variant="contained" color="secondary" disabled>
      Pay & Download
    </Button>
  </Box>
);

export default Payment;
