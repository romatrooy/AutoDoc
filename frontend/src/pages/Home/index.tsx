import { Typography, Paper, Box } from '@mui/material';

const Home = () => {
  return (
    <Paper sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Welcome to AutoDoc
      </Typography>
      <Typography variant="body1">
        Automated document filling system
      </Typography>
    </Paper>
  );
};

export default Home;
