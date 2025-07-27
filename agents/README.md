# SaaS Validator Agent

A LangGraph-based agent that validates SaaS business ideas using Google Trends data through HTTP API server integration.

## Features

- 🤖 **LangGraph Agent**: Built with LangGraph for complex workflow orchestration
- 📊 **Google Trends Integration**: Fetches real-time trends data via HTTP API server
- 💡 **Business Intelligence**: Analyzes market demand and provides actionable recommendations
- 🔄 **Modular Design**: Easy to extend with additional data sources (Meta, LinkedIn, etc.)
- 🚀 **Anthropic Claude**: Powered by Claude 3.5 Sonnet for intelligent analysis

## Architecture

```
User Query → Query Analysis → Google Trends API → Data Analysis → Recommendations
     ↓              ↓              ↓              ↓              ↓
LangGraph → HTTP Client → Google Trends Server → Claude Analysis → Business Insights
```

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Keys

The Anthropic API key is already configured in `config.py`. The Google Trends API server URL is set to `http://localhost:8000` by default.

### 3. Start Google Trends API Server

Make sure your Google Trends HTTP API server is running:

```bash
# In your Google Trends MCP server directory
source venv/bin/activate
./venv/bin/python run_api_server.py
```

The server should be running at `http://localhost:8000`.

## Usage

### Interactive Mode

Run the agent in interactive mode to ask questions:

```bash
python run_agent.py
```

### Demo with Google Trends

Run the complete demo with Google Trends integration:

```bash
python demo_with_trends.py
```

### Single Query Mode

Run the agent for a single query:

```bash
python run_agent.py "What are the trends in remote work software?"
```

### Programmatic Usage

```python
import asyncio
from saas_validator_agent import SaaSValidatorAgent

async def main():
    agent = SaaSValidatorAgent()
    result = await agent.run("Should I build a SaaS for AI-powered project management?")
    
    if result["success"]:
        print("Recommendations:", result["recommendations"])
        print("Trends data:", result["trends_data"])
    else:
        print("Error:", result["error"])

asyncio.run(main())
```

## Agent Workflow

1. **Query Analysis**: Analyzes the user query to determine if Google Trends data is needed
2. **Trends Fetching**: Connects to Google Trends HTTP API server to fetch data
3. **Data Analysis**: Uses Claude to analyze trends and extract insights
4. **Recommendations**: Generates actionable business recommendations

## Google Trends API Integration

The agent communicates with Google Trends through an HTTP API server. Available endpoints:

- `/trending` - Get trending searches
- `/related-queries` - Get related queries for keywords
- `/related-topics` - Get related topics for keywords
- `/geographic-interest` - Get geographic interest data
- `/interest-over-time` - Get interest over time data

### API Response Format

```json
{
  "success": true,
  "data": {
    // Response data here
  },
  "error": null,
  "timestamp": "2024-01-01T12:00:00"
}
```

## Configuration

### Environment Variables

- `ANTHROPIC_API_KEY`: Your Anthropic API key (already configured)
- `GOOGLE_TRENDS_API_URL`: Your Google Trends API server URL (default: http://localhost:8000)

### Model Configuration

The agent uses Claude 3.5 Sonnet with:
- Temperature: 0.1 (for consistent, focused responses)
- Model: claude-3-5-sonnet-20241022

## Testing

### Run All Tests

```bash
python test_agent.py
```

### Test Google Trends Integration

```bash
python test_google_trends.py
```

## Error Handling

The agent includes comprehensive error handling:
- Google Trends API server connection failures
- API rate limiting
- Invalid queries
- Network timeouts

## Development

### Running Tests

```bash
python -m pytest tests/
```

### Adding New Features

1. Create feature branch
2. Add new nodes to the LangGraph workflow
3. Update the state model if needed
4. Add tests
5. Submit pull request

## Troubleshooting

### Common Issues

1. **Google Trends API Server Not Running**
   - Check if the server is running at http://localhost:8000
   - Verify the server health with: `curl http://localhost:8000/health`

2. **API Key Issues**
   - Verify the Anthropic API key is valid
   - Check API usage limits

3. **Import Errors**
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Check Python version (3.8+ required)

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## Support

For issues and questions:
- Create an issue on GitHub
- Check the troubleshooting section
- Review the documentation 