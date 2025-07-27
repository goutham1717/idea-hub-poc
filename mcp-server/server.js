import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import { getJson } from 'serpapi';

dotenv.config();

const app = express();
const PORT = process.env.PORT || 3010;
const SERPAPI_KEY = process.env.serpapi_key

app.use(cors());
app.use(express.json());

app.get('/api/trends', async (req, res) => {
  try {
    const { keywords, date = 'today 12-m' } = req.query;

    if (!keywords) {
      return res.status(400).json({
        error: 'Keywords parameter is required. Use comma-separated values like: ?keywords=coffee,milk,bread'
      });
    }

    const q = keywords.split(',').map(k => k.trim()).filter(k => k.length > 0).join(',');
    if (!q) {
      return res.status(400).json({ error: 'At least one valid keyword is required' });
    }

    // Call SerpApi
    getJson({
      engine: "google_trends",
      q,
      data_type: "TIMESERIES",
      api_key: SERPAPI_KEY
    }, (json) => {
      if (json.error) {
        return res.status(500).json({ error: json.error });
      }
      console.log("Trends response: ", JSON.stringify(json, null, 2));
      res.json(json);
    });

  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.get('/api/health', (req, res) => {
  res.json({ status: 'OK', message: 'Google Trends Server (SerpApi) is running' });
});

app.listen(PORT, () => {
  console.log(`Google Trends Server (SerpApi) running on http://localhost:${PORT}`);
  console.log('  GET /api/trends?keywords=coffee,milk,bread,pasta,steak');
  console.log('  GET /api/health');
}); 