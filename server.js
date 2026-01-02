const express = require('express');
const cors = require('cors');
const fetch = require('node-fetch'); // Ensure you have node-fetch installed
const app = express();
const port = 3001;

app.use(cors()); // Allow all origins, methods, and headers
app.use(express.json()); // Middleware to parse JSON bodies

// In-memory storage for saved prompts
let savedPrompts = [];

// Endpoint to get saved prompts
app.get('/prompts', (req, res) => {
  res.json({ savedPrompts });
});

// Endpoint to save a new prompt
app.post('/prompts', (req, res) => {
  const { prompt } = req.body;
  if (prompt) {
    savedPrompts.push(prompt);
    res.json({ message: 'Prompt saved.', savedPrompts });
  } else {
    res.status(400).json({ message: 'Prompt is required.' });
  }
});

// Endpoint to fetch response from Gemini API
app.post('/gemini', async (req, res) => {
  const { prompt } = req.body;
  
  if (!prompt) {
    return res.status(400).json({ message: 'Prompt is required.' });
  }

  const geminiApiKey = 'YOUR_GEMINI_API_KEY'; // Replace with your actual Gemini API key

  try {
    // Constructing the prompt to explicitly ask for relevant links
    const enhancedPrompt = `${prompt}\n\nPlease provide three relevant website links related to the topic.`;

    const response = await fetch(
      `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key=${geminiApiKey}`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          contents: [
            {
              parts: [
                {
                  text: enhancedPrompt,
                },
              ],
            },
          ],
        }),
      }
    );

    const data = await response.json();
    const generatedContent = data.candidates[0]?.content.parts[0]?.text || '';

    // Function to extract up to 3 URLs from the generated content
    const extractUrls = (content) => {
      const urlRegex = /(https?:\/\/[^\s]+)/g; // Regex pattern to match URLs
      const matches = content.match(urlRegex); // Find all URL matches
      return matches ? matches.slice(0, 3) : []; // Return the first 3 matches or an empty array
    };

    const websites = extractUrls(generatedContent);

    // If URLs are found, respond with them; otherwise, notify no links were found
    if (websites.length > 0) {
      res.json({ message: 'Top 3 links found:', links: websites });
    } else {
      res.json({ message: 'No links found in the response.' });
    }
    
  } catch (error) {
    console.error('Error fetching response:', error.message);
    res.status(500).json({ message: 'Error fetching response.', error: error.message });
  }
});

app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});