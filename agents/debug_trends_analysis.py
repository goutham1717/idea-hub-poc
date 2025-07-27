#!/usr/bin/env python3
"""
Debug script for trends analysis
"""

import asyncio
import os
import json
from saas_validator_agent import SaaSValidatorAgent

async def debug_trends_analysis():
    """Debug the trends analysis functionality"""
    
    # Set environment variables
    os.environ["ANTHROPIC_API_KEY"] = "your-anthropic-api-key-here"
    os.environ["GOOGLE_TRENDS_API_URL"] = "http://localhost:3010"
    
    print("🔍 Debugging Trends Analysis")
    print("=" * 50)
    
    # Initialize the agent
    agent = SaaSValidatorAgent()
    
    # Test query
    query = "Can I set up a cafe in Chennai?"
    
    print(f"Query: {query}")
    
    try:
        # Test keyword generation
        print("\n1. Testing keyword generation...")
        keywords = await agent._generate_keywords_from_query(query)
        print(f"Generated keywords: {keywords}")
        
        # Test trends fetching
        print("\n2. Testing trends fetching...")
        trends_data = await agent._fetch_trends([query])
        print(f"Trends data received: {trends_data is not None}")
        if trends_data:
            print(f"Trends data keys: {list(trends_data.keys())}")
        
        # Test trends analysis
        if trends_data:
            print("\n3. Testing trends analysis...")
            analysis = await agent._analyze_trends_and_score(trends_data)
            print(f"Analysis result: {analysis}")
        
        # Test full recommendation generation
        print("\n4. Testing full recommendation generation...")
        recommendations = await agent._generate_recommendations(query, trends_data)
        print(f"Number of recommendations: {len(recommendations)}")
        for i, rec in enumerate(recommendations):
            print(f"Recommendation {i+1}: {rec[:100]}...")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(debug_trends_analysis()) 