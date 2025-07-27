# Idea Hub POC

A multi-component SaaS application with dedicated frontend, backend, and AI components.

## Project Structure

This project is organized into separate components, each with its own technology stack and responsibilities:

### 📁 `saas-frontend/`
Frontend application component - handles user interface and client-side functionality.

### 📁 `saas-backend/`
Backend API and server component - manages business logic, database operations, and API endpoints.

### 📁 `mcp-server/`
MCP (Model Context Protocol) server component - handles AI/ML model serving and inference.

### 📁 `agents/`
AI agents component - contains intelligent agents and automation logic.

## Getting Started

Each component has its own setup and configuration. Please refer to the individual README files in each directory for specific setup instructions.

### 🔑 API Keys Configuration

This project requires several API keys for full functionality:

#### **SerpAPI Key**
1. Visit [SerpAPI Dashboard](https://serpapi.com/dashboard)
2. Sign up for an account or sign in if you already have one
3. Navigate to your API keys section
4. Copy your API key
5. Set it as an environment variable:
   ```bash
   export SERPAPI_KEY="your-serpapi-key-here"
   ```

#### **Anthropic API Key**
1. Visit [Anthropic Console](https://console.anthropic.com/)
2. Create an account or sign in
3. Generate a new API key
4. Set it as an environment variable:
   ```bash
   export ANTHROPIC_API_KEY="your-anthropic-api-key-here"
   ```

### 📝 Environment Variables
Create a `.env` file in the root directory with your API keys:
```bash
# API Keys
SERPAPI_KEY=your-serpapi-key-here
ANTHROPIC_API_KEY=your-anthropic-api-key-here

# Service URLs
GOOGLE_TRENDS_API_URL=http://localhost:3010
```

## Development

This is a monorepo structure where each component can be developed and deployed independently while sharing common configurations and utilities.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

[Add your license information here]
