"""
Example LangGraph integration with Google Trends Mock Server

This example shows how to use the Google Trends Mock Server with LangGraph
to create an AI agent that can analyze trends data.
"""

import httpx
import asyncio
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

# Define the state for our agent
class AgentState(TypedDict):
    query: str
    keywords: list
    trends_data: dict
    analysis: str
    response: str

# Function to get trends data from our server
async def get_trends_data(state: AgentState) -> AgentState:
    """Get Google Trends data for the keywords"""
    try:
        # Convert keywords list to comma-separated string
        keywords_str = ','.join(state["keywords"])
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "http://localhost:3010/api/trends",
                params={"keywords": keywords_str}
            )
            if response.status_code == 200:
                state["trends_data"] = response.json()
            else:
                state["trends_data"] = {"error": f"Failed to get trends: {response.status_code}"}
    except Exception as e:
        state["trends_data"] = {"error": f"Exception: {str(e)}"}
    return state

# Function to analyze trends data
def analyze_trends(state: AgentState) -> AgentState:
    """Analyze the trends data and provide insights"""
    trends = state["trends_data"]
    
    if "error" in trends:
        state["analysis"] = f"Error getting trends data: {trends['error']}"
        return state
    
    try:
        # Extract timeline data
        timeline_data = trends.get("interest_over_time", {}).get("timeline_data", [])
        averages = trends.get("interest_over_time", {}).get("averages", [])
        
        if not timeline_data:
            state["analysis"] = "No trends data available for these keywords."
            return state
        
        # Get recent data points (last 4 weeks)
        recent_data = timeline_data[-4:] if len(timeline_data) >= 4 else timeline_data
        
        # Generate analysis for each keyword
        analysis_parts = []
        analysis_parts.append(f"Trends Analysis for keywords: {', '.join(state['keywords'])}")
        analysis_parts.append("=" * 50)
        
        for avg in averages:
            keyword = avg["query"]
            avg_value = avg["value"]
            
            # Get recent values for this keyword
            recent_values = []
            for week in recent_data:
                keyword_value = next((v for v in week["values"] if v["query"] == keyword), None)
                if keyword_value:
                    recent_values.append(keyword_value["extracted_value"])
            
            if recent_values:
                current_trend = recent_values[-1]
                trend_direction = "increasing" if recent_values[-1] > recent_values[0] else "decreasing" if recent_values[-1] < recent_values[0] else "stable"
                
                analysis_parts.append(f"\n{keyword.upper()}:")
                analysis_parts.append(f"  - Average interest: {avg_value}")
                analysis_parts.append(f"  - Current trend: {current_trend}")
                analysis_parts.append(f"  - Trend direction: {trend_direction}")
                analysis_parts.append(f"  - Recent 4-week average: {sum(recent_values) / len(recent_values):.1f}")
        
        # Overall insights
        analysis_parts.append(f"\nOverall Insights:")
        analysis_parts.append(f"  - Data points analyzed: {len(timeline_data)} weeks")
        analysis_parts.append(f"  - Date range: {timeline_data[0]['date']} to {timeline_data[-1]['date']}")
        
        # Find highest and lowest average keywords
        if averages:
            highest = max(averages, key=lambda x: x["value"])
            lowest = min(averages, key=lambda x: x["value"])
            analysis_parts.append(f"  - Highest average interest: {highest['query']} ({highest['value']})")
            analysis_parts.append(f"  - Lowest average interest: {lowest['query']} ({lowest['value']})")
        
        state["analysis"] = "\n".join(analysis_parts)
        
    except Exception as e:
        state["analysis"] = f"Error analyzing trends: {str(e)}"
    
    return state

# Function to generate final response
def generate_response(state: AgentState) -> AgentState:
    """Generate the final response based on analysis"""
    analysis = state["analysis"]
    keywords = state["keywords"]
    
    response = f"""
Based on Google Trends analysis for: {', '.join(keywords)}

{analysis}

This data shows the relative search interest over time. Higher values indicate more searches relative to the total number of searches.
    """.strip()
    
    state["response"] = response
    return state

# Build the workflow graph
def create_workflow() -> StateGraph:
    """Create the LangGraph workflow"""
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("get_trends", get_trends_data)
    workflow.add_node("analyze_trends", analyze_trends)
    workflow.add_node("generate_response", generate_response)
    
    # Set entry point
    workflow.set_entry_point("get_trends")
    
    # Add edges
    workflow.add_edge("get_trends", "analyze_trends")
    workflow.add_edge("analyze_trends", "generate_response")
    workflow.add_edge("generate_response", END)
    
    return workflow.compile()

# Example usage
async def main():
    """Example usage of the trends analysis agent"""
    
    # Create the workflow
    app = create_workflow()
    
    # Test with different keyword sets
    test_queries = [
        {
            "query": "Food trends",
            "keywords": ["coffee", "milk", "bread", "pasta", "steak"]
        },
        {
            "query": "Tech trends", 
            "keywords": ["artificial intelligence", "machine learning", "blockchain", "cryptocurrency"]
        },
        {
            "query": "Social media trends",
            "keywords": ["instagram", "tiktok", "facebook", "twitter", "youtube"]
        }
    ]
    
    for test in test_queries:
        print(f"\n{'='*60}")
        print(f"Analyzing trends for: {test['query']}")
        print(f"Keywords: {', '.join(test['keywords'])}")
        print(f"{'='*60}")
        
        # Run the workflow
        result = await app.ainvoke({
            "query": test["query"],
            "keywords": test["keywords"]
        })
        
        print(result["response"])
        print()

if __name__ == "__main__":
    # Make sure the Google Trends Mock Server is running on localhost:3010
    print("Make sure the Google Trends Mock Server is running on localhost:3010")
    print("Run: npm start in the server directory")
    print()
    
    # Run the example
    asyncio.run(main()) 