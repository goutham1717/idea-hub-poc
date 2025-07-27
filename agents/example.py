#!/usr/bin/env python3
"""
Example usage of the SaaS Validator Agent

This script demonstrates how to use the agent programmatically
and shows different types of queries and responses.
"""

import asyncio
import json
from saas_validator_agent import SaaSValidatorAgent
from config import Config

async def example_basic_analysis():
    """Example of basic business analysis without trends data"""
    print("📊 Example 1: Basic Business Analysis")
    print("=" * 50)
    
    agent = SaaSValidatorAgent()
    
    query = "What are the key success factors for a B2B SaaS startup?"
    print(f"Query: {query}")
    print()
    
    result = await agent.run(query)
    
    if result["success"]:
        print("✅ Analysis completed successfully!")
        print("\n💡 Recommendations:")
        for i, rec in enumerate(result["recommendations"], 1):
            print(f"{i}. {rec}")
    else:
        print(f"❌ Error: {result['error']}")
    
    print("\n" + "="*50 + "\n")

async def example_market_research():
    """Example of market research with trends data (when MCP server is available)"""
    print("📈 Example 2: Market Research with Trends")
    print("=" * 50)
    
    agent = SaaSValidatorAgent()
    
    query = "Should I build a SaaS for AI-powered customer support?"
    print(f"Query: {query}")
    print()
    
    result = await agent.run(query)
    
    if result["success"]:
        print("✅ Analysis completed successfully!")
        
        if result.get("trends_data"):
            print(f"📊 Trends data retrieved for {len(result['trends_data'])} queries")
            for query, data in result["trends_data"].items():
                print(f"  - {query}: {json.dumps(data, indent=2)}")
        
        print("\n💡 Recommendations:")
        for i, rec in enumerate(result["recommendations"], 1):
            print(f"{i}. {rec}")
    else:
        print(f"❌ Error: {result['error']}")
    
    print("\n" + "="*50 + "\n")

async def example_competitive_analysis():
    """Example of competitive analysis"""
    print("🏆 Example 3: Competitive Analysis")
    print("=" * 50)
    
    agent = SaaSValidatorAgent()
    
    query = "How can I differentiate my project management SaaS from competitors?"
    print(f"Query: {query}")
    print()
    
    result = await agent.run(query)
    
    if result["success"]:
        print("✅ Analysis completed successfully!")
        print("\n💡 Recommendations:")
        for i, rec in enumerate(result["recommendations"], 1):
            print(f"{i}. {rec}")
    else:
        print(f"❌ Error: {result['error']}")
    
    print("\n" + "="*50 + "\n")

async def example_error_handling():
    """Example of error handling"""
    print("⚠️  Example 4: Error Handling")
    print("=" * 50)
    
    agent = SaaSValidatorAgent()
    
    # Test with an empty query
    query = ""
    print(f"Query: '{query}' (empty query)")
    print()
    
    result = await agent.run(query)
    
    if result["success"]:
        print("✅ Analysis completed successfully!")
        print("\n💡 Recommendations:")
        for i, rec in enumerate(result["recommendations"], 1):
            print(f"{i}. {rec}")
    else:
        print(f"❌ Error: {result['error']}")
    
    print("\n" + "="*50 + "\n")

async def example_batch_processing():
    """Example of processing multiple queries in batch"""
    print("🔄 Example 5: Batch Processing")
    print("=" * 50)
    
    agent = SaaSValidatorAgent()
    
    queries = [
        "What pricing model works best for SaaS?",
        "How to validate a SaaS idea quickly?",
        "What are the biggest SaaS challenges?"
    ]
    
    results = []
    
    for i, query in enumerate(queries, 1):
        print(f"Processing query {i}/{len(queries)}: {query}")
        result = await agent.run(query)
        results.append(result)
    
    print("\n📊 Batch Results Summary:")
    print("-" * 30)
    
    successful = sum(1 for r in results if r["success"])
    print(f"✅ Successful analyses: {successful}/{len(queries)}")
    
    for i, result in enumerate(results, 1):
        status = "✅" if result["success"] else "❌"
        print(f"{status} Query {i}: {result['query'][:50]}...")
    
    print("\n" + "="*50 + "\n")

async def main():
    """Run all examples"""
    print("🚀 SaaS Validator Agent - Examples")
    print("=" * 60)
    
    # Validate configuration first
    try:
        Config.validate()
        print("✅ Configuration validated")
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return
    
    # Run examples
    await example_basic_analysis()
    await example_market_research()
    await example_competitive_analysis()
    await example_error_handling()
    await example_batch_processing()
    
    print("🎉 All examples completed!")

if __name__ == "__main__":
    asyncio.run(main()) 