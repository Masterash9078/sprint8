const express = require('express');
const { spawn } = require('child_process');
const cors = require('cors'); // Import CORS

const app = express();

// Configure CORS with options
const corsOptions = {
  origin: 'http://localhost:3000', // Allow only this origin
  methods: ['GET', 'POST'], // Allow these HTTP methods
  credentials: true, // Allow credentials if needed (for cookies, authorization headers, etc.)
};

app.use(cors(corsOptions)); // Use CORS with the options

// Function to run the Python script
function runPythonScript(scriptFunction, args) {
  return new Promise((resolve, reject) => {
    const pythonProcess = spawn('python3', ['script.py', scriptFunction, ...args]);

    let dataString = '';

    pythonProcess.stdout.on('data', (data) => {
      console.log('Received data from Python script:', data.toString());
      dataString += data.toString();
    });

    pythonProcess.stderr.on('data', (data) => {
      console.error('Error from Python script:', data.toString());
    });

    pythonProcess.on('close', (code) => {
      console.log(`Python script finished with exit code ${code}`);
      console.log('Full data received:', dataString);

      try {
        const jsonData = JSON.parse(dataString);
        resolve(jsonData);
      } catch (error) {
        reject({
          error: 'Failed to parse data',
          details: error.message,
          rawData: dataString,
        });
      }
    });
  });
}

// Endpoint for production data
app.get('/api/production-data', async (req, res) => {
  const { plant, item } = req.query;
 
  if (!plant || !item) {
    return res.status(400).json({ error: 'Both plant and item are required' });
  }

  console.log(`Received request for production data with Plant: ${plant}, Item: ${item}`);

  try {
    const result = await runPythonScript('card_1', [plant, item]);
    res.json(result);
  } catch (error) {
    res.status(500).json(error);
  }
});

// Endpoint for MRP data
app.get('/api/mrp-data', async (req, res) => {
  const { plant, material } = req.query;
 
  if (!plant || !material) {
    return res.status(400).json({ error: 'Both plant and material are required' });
  }

  console.log(`Received request for MRP data with Plant: ${plant}, Material: ${material}`);

  try {
    const result = await runPythonScript('card_2', [plant, material]);
    res.json(result);
  } catch (error) {
    res.status(500).json(error);
  }
});

// Start the server
app.listen(3001, () => {
  console.log('Server running on port 3001');
});
