# Google Trends Mock Server

A Node.js server that provides mock Google Trends data through REST API endpoints. This server is designed to be used with AI agents built using LangGraph or other applications that need Google Trends data for development and testing.

## Features

- **Mock Data Generation**: Dynamic mock data using faker library
- **REST API**: Single endpoint for trends data with multiple keywords
- **Realistic Data**: Generates 52 weeks of realistic trend patterns
- **Flexible Keywords**: Support for multiple keywords in a single request
- **Error Handling**: Comprehensive error handling and validation
- **CORS Support**: Cross-origin requests enabled for web applications

## Installation

1. Clone or download this repository
2. Install dependencies:
   ```bash
   npm install
   ```

## Usage

### Starting the Server

```bash
npm start
```

Or for development with auto-restart:
```bash
npm run dev
```

The server will start on port 3010 (or the port specified in your `.env` file).

### REST API Endpoints

#### 1. Trends Data
Get mock Google Trends data for multiple keywords.

```
GET /api/trends?keywords=<keyword1,keyword2,keyword3>&date=<date_range>
```

**Parameters:**
- `keywords` (required): Comma-separated list of keywords
- `date` (optional): Date range (default: "today 12-m")

**Example:**
```bash
curl "http://localhost:3010/api/trends?keywords=coffee,milk,bread,pasta,steak"
```

**Response Format:**
```json
{
  "search_metadata": {
    "id": "628e1083de983400a3b29c2e",
    "status": "Success",
    "created_at": "2022-05-25 11:18:27 UTC",
    "total_time_taken": 1.89
  },
  "search_parameters": {
    "engine": "google_trends",
    "q": "coffee,milk,bread,pasta,steak",
    "date": "today 12-m",
    "data_type": "TIMESERIES"
  },
  "interest_over_time": {
    "timeline_data": [
      {
        "date": "May 30 – Jun 5, 2021",
        "timestamp": "1622304000",
        "values": [
          {
            "query": "coffee",
            "value": "80",
            "extracted_value": 80
          },
          {
            "query": "milk",
            "value": "58",
            "extracted_value": 58
          }
        ]
      }
    ],
    "averages": [
      {
        "query": "coffee",
        "value": 84
      },
      {
        "query": "milk",
        "value": 55
      }
    ]
  }
}
```

#### 2. Health Check
Check if the server is running.

```
GET /api/health
```

**Example:**
```bash
curl "http://localhost:3010/api/health"
```

## Integration with LangGraph

Here are several ways to integrate this server with your LangGraph AI agent:

### Method 1: Direct HTTP Requests

```python
import httpx
from langgraph.graph import StateGraph, END
from typing import TypedDict

# Define your state
class AgentState(TypedDict):
    query: str
    keywords: list
    trends_data: dict
    response: str

# Function to get trends data
async def get_trends_data(state: AgentState) -> AgentState:
    async with httpx.AsyncClient() as client:
        keywords_str = ','.join(state["keywords"])
        response = await client.get(
            "http://localhost:3010/api/trends",
            params={"keywords": keywords_str}
        )
        state["trends_data"] = response.json()
    return state

# Function to generate response using trends data
def generate_response(state: AgentState) -> AgentState:
    trends = state["trends_data"]
    averages = trends["interest_over_time"]["averages"]
    
    analysis = "Trends Analysis:\n"
    for avg in averages:
        analysis += f"- {avg['query']}: {avg['value']}\n"
    
    state["response"] = analysis
    return state

# Build your graph
workflow = StateGraph(AgentState)
workflow.add_node("get_trends", get_trends_data)
workflow.add_node("generate_response", generate_response)
workflow.set_entry_point("get_trends")
workflow.add_edge("get_trends", "generate_response")
workflow.add_edge("generate_response", END)

app = workflow.compile()
```

### Method 2: Using LangGraph Tools

```python
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
import httpx

# Define a tool for getting trends data
async def get_google_trends(keywords: str) -> dict:
    """Get Google Trends data for keywords"""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://localhost:3010/api/trends",
            params={"keywords": keywords}
        )
        return response.json()

# Create tool node
tools = [get_google_trends]
tool_node = ToolNode(tools)

# Use in your graph
workflow = StateGraph(AgentState)
workflow.add_node("tools", tool_node)
# ... rest of your graph
```

### Method 3: Custom Tool Integration

```python
from langchain.tools import BaseTool
import httpx

class GoogleTrendsTool(BaseTool):
    name = "google_trends"
    description = "Get Google Trends data for keywords"
    
    def _run(self, keywords: str) -> str:
        response = httpx.get(
            "http://localhost:3010/api/trends",
            params={"keywords": keywords}
        )
        return str(response.json())
    
    async def _arun(self, keywords: str) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "http://localhost:3010/api/trends",
                params={"keywords": keywords}
            )
            return str(response.json())

# Use in your LangGraph agent
tools = [GoogleTrendsTool()]
```

## Environment Variables

Create a `.env` file in the root directory to configure the server:

```env
PORT=3010
```

## Testing

You can test the server using the provided examples:

```bash
# Test the server
node test_server.js

# Run the example
node example.js

# Test individual endpoints
curl "http://localhost:3010/api/trends?keywords=coffee,milk,bread"
```

## Mock Data Features

- **52 weeks of data**: Generates a full year of weekly data points
- **Realistic patterns**: Uses faker to generate realistic trend variations
- **Multiple keywords**: Supports comparing multiple keywords in a single request
- **Dynamic averages**: Calculates realistic averages for each keyword
- **Consistent format**: Matches the expected Google Trends API response format

## Error Handling

The server includes comprehensive error handling:
- Input validation for required parameters
- Proper HTTP status codes for different error types
- Detailed error messages for debugging

## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT License 