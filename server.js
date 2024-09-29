const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const Client = require('./models/Client'); // Assuming you have a Client model
// Import the Portfolio model
const Portfolio = require('./models/Portfolio');
const Dailyrisk = require('./models/Dailyrisk');
const DailySentiment = require('./models/DailySentiment');
const ClientSatisfaction = require('./models/ClientSatisfaction');
const { spawn } = require('child_process');
// Create Express app
const app = express();
app.use(cors());
app.use(express.json()); // Parse JSON request bodies

// MongoDB Connection URI
const mongoURI = 'mongodb+srv://svishnu1:VdxX20O4McH5g4vI@cluster0.zdttw.mongodb.net/client_analysis?retryWrites=true&w=majority';



mongoose.connect(mongoURI)
  .then(() => console.log('MongoDB connected successfully'))
  .catch(err => console.error('MongoDB connection error:', err));


// API route to get all clients
app.get('/api/clients', async (req, res) => {
    try {
        const clients = await Client.find();
        res.json(clients);
    } catch (err) {
        res.status(500).json({ error: 'Server error' });
    }
});



// API route to get a specific portfolio by client_id
app.get('/api/portfolios/:client_id', async (req, res) => {
    try {
        // Use find() to get all portfolios matching the client_id
        const portfolios = await Portfolio.find({ client_id: req.params.client_id });

        // If no portfolios are found, return a 404 error
        if (portfolios.length === 0) {
            return res.status(404).json({ error: 'No portfolios found for this client' });
        }

        console.log('All portfolios found with find():', portfolios); // Log all portfolios

        // Now use findOne() to get the first portfolio
        const firstPortfolio = await Portfolio.findOne({ client_id: req.params.client_id });

        if (!firstPortfolio) {
            return res.status(404).json({ error: 'Portfolio not found' });
        }

        console.log('First portfolio found with findOne():', firstPortfolio); // Log first portfolio

        // Send the first portfolio found as a JSON response
        res.json(firstPortfolio);

    } catch (err) {
        console.error('Server error:', err);
        res.status(500).json({ error: 'Server error' });
    }
});

// app.get('/api/dailyrisks', async (req, res) => {
//     try {
//       const dailyrisks = await Dailyrisk.find(); // Fetch all daily risk entries
//       console.log('Daily Risks:', dailyrisks);   // Log the retrieved data to check if the query works
//       res.json(dailyrisks);                      // Return the data as JSON
//     } catch (err) {
//       console.error('Error fetching daily risks:', err);
//       res.status(500).json({ error: 'Server error' });
//     }
//   });
  
  app.get('/api/dailyrisks/:client_id', async (req, res) => {
    try {
      const clientId = req.params.client_id;  // Get client_id from URL params
      const dailyrisks = await Dailyrisk.find({ client_id: clientId });  // Fetch daily risks for the given client_id
  
      // If no daily risks are found, return a 404 response
      if (dailyrisks.length === 0) {
        return res.status(404).json({ error: `No daily risks found for client_id: ${clientId}` });
      }
  
      // Log the retrieved data and return it as JSON
      console.log('Daily Risks for client_id', clientId, ':', dailyrisks);
      res.json(dailyrisks);  // Return the data as JSON
    } catch (err) {
      console.error('Error fetching daily risks:', err);
      res.status(500).json({ error: 'Server error' });
    }
  });
//   app.get('/api/dailysentiments', async (req, res) => {
//     try {
//       const dailySentiments = await DailySentiment.find(); // Fetch all daily sentiment entries
//       console.log('Daily Sentiments:', dailySentiments);   // Log the retrieved data to check if the query works
//       res.json(dailySentiments);                           // Return the data as JSON
//     } catch (err) {
//       console.error('Error fetching daily sentiments:', err); // Log any errors
//       res.status(500).json({ error: 'Server error' });        // Return a 500 status with an error message
//     }
//   });
  

 // API route to get daily sentiments by client_id
app.get('/api/dailysentiments/:client_id', async (req, res) => {
    try {
      const clientId = req.params.client_id;  // Get client_id from URL params
      const dailySentiments = await DailySentiment.find({ client_id: clientId });  // Fetch daily sentiments for the given client_id
  
      // If no daily sentiments are found, return a 404 response
      if (dailySentiments.length === 0) {
        return res.status(404).json({ error: `No daily sentiments found for client_id: ${clientId}` });
      }
  
      // Log the retrieved data and return it as JSON
      console.log('Daily Sentiments for client_id', clientId, ':', dailySentiments);
      res.json(dailySentiments);  // Return the data as JSON
    } catch (err) {
      console.error('Error fetching daily sentiments:', err);
      res.status(500).json({ error: 'Server error' });
    }

  });


// In server.js or client routes
app.get('/api/clients/:client_id', async (req, res) => {
    try {
      const client = await Client.findOne({ client_id: req.params.client_id });
      if (!client) {
        return res.status(404).json({ error: 'Client not found' });
      }
      console.log(client);
      res.json(client);
    } catch (err) {
      console.log(err);
      res.status(500).json({ error: 'Server error' });
    }
  });

  app.get('/api/clientSatisfactions/:client_id', async (req, res) => {
    try {
      const satisfaction = await ClientSatisfaction.findOne({ client_id: req.params.client_id });
  
      if (!satisfaction) {
        return res.status(404).json({ error: 'Client satisfaction data not found' });
      }
  
      res.json(satisfaction);
    } catch (err) {
      console.error('Error fetching client satisfaction data:', err);
      res.status(500).json({ error: 'Server error' });
    }
  });
  
  app.get('/api/clientSatisfactions', async (req, res) => {
    try {
      const satisfactions = await ClientSatisfaction.find(); // Fetch all client satisfaction data
      if (!satisfactions.length) {
        return res.status(404).json({ error: 'No client satisfaction data found' });
      }
  
      res.json(satisfactions);
    } catch (err) {
      console.error('Error fetching client satisfaction data:', err);
      res.status(500).json({ error: 'Server error' });
    }
  });

// API route to get all portfolios
app.get('/api/portfolios', async (req, res) => {
    try {
        const portfolios = await Portfolio.find(); // Fetch all portfolios from the database
        console.log(portfolios);
        res.json(portfolios); // Return portfolios as JSON
    } catch (err) {
        console.error('Error fetching portfolios:', err);
        res.status(500).json({ error: 'Server error' });
    }
});

app.get('/run-python', (req, res) => {
  // Spawn the Python process
  const python = spawn('python3', ['./python_scripts/main.py']);
    // Capture stdout (standard output)
    python.stdout.on('data', (data) => {
      console.log(`stdout: ${data.toString()}`);
    });
  
    // Capture stderr (error output) to see if any errors are occurring
    python.stderr.on('data', (data) => {
      console.error(`stderr: ${data.toString()}`);
    });
  
   

  // Simply respond that the script was triggered
  // res.send('Python script has been triggered successfully!');
});


// Start the server
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
