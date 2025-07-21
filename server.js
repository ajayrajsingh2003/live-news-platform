const express = require('express');
const path = require('path');
const app = express();
const PORT = process.env.PORT || 3000;

// Serve static files
app.use(express.static(__dirname));

// Handle all routes by serving the main HTML file
app.get('*', (req, res) => {
  res.sendFile(path.resolve(__dirname, 'wcindex.html'));
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
