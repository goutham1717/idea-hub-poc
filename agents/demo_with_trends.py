#!/usr/bin/env python3
"""
Demo script for SaaS Validator Agent with Google Trends Integration

This script demonstrates the complete functionality of the agent
with real Google Trends data from the HTTP API server.
"""

import asyncio
import sys
import os

# Add the current directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from saas_validator_agent import SaaSValidatorAgent
from config import Config

async def demo_agent():
    """Demo the SaaS Validator agent with Google Trends integration"""
    print("🚀 SaaS Validator Agent - Google Trends Integration Demo")
    print("=" * 70)
    print("This demo shows how the agent validates SaaS business ideas")
    print("using real Google Trends data from the HTTP API server.")
    print()
    
    # Validate configuration
    try:
        Config.validate()
        print("✅ Configuration validated")
        print(f"✅ Google Trends API: {Config.GOOGLE_TRENDS_API_URL}")
        print()
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return
    
    # Create agent
    agent = SaaSValidatorAgent()
    
    # Demo queries that showcase different aspects
    demo_queries = [
        {
            "query": "Should I build a SaaS for AI-powered customer support?",
            "description": "AI Customer Support SaaS"
        },
        {
            "query": "What are the trends in remote work productivity tools?",
            "description": "Remote Work Tools Analysis"
        },
        {
            "query": "Is there market demand for a new project management solution?",
            "description": "Project Management Market"
        }
    ]
    
    for i, demo in enumerate(demo_queries, 1):
        print(f"📊 Demo {i}: {demo['description']}")
        print("=" * 50)
        print(f"Query: {demo['query']}")
        print()
        
        try:
            print("🤔 Analyzing query and fetching Google Trends data...")
            result = await agent.run(demo['query'])
            
            if result["success"]:
                print("✅ Analysis completed successfully!")
                
                # Show trends data summary
                if result.get("trends_data"):
                    print(f"\n📈 Google Trends Data Retrieved:")
                    for query, data in result["trends_data"].items():
                        print(f"  - Query: {query}")
                        if "interest_over_time" in data:
                            print(f"    • Interest over time data available")
                        if "related_queries" in data:
                            print(f"    • Related queries data available")
                        if "related_topics" in data:
                            print(f"    • Related topics data available")
                        if "geographic_interest" in data:
                            print(f"    • Geographic interest data available")
                else:
                    print("\n📊 No trends data needed for this query")
                
                # Show recommendations
                print(f"\n💡 Business Recommendations:")
                for j, rec in enumerate(result["recommendations"], 1):
                    print(f"{j}. {rec}")
                    
            else:
                print(f"❌ Analysis failed: {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            print(f"❌ Demo failed with exception: {e}")
        
        print("\n" + "="*70 + "\n")

async def interactive_demo():
    """Interactive demo where user can ask questions"""
    print("🎯 Interactive SaaS Validator Demo")
    print("=" * 50)
    print("Ask any SaaS business question and get AI-powered recommendations!")
    print("Type 'quit' to exit.")
    print()
    
    agent = SaaSValidatorAgent()
    
    while True:
        try:
            query = input("💬 Enter your SaaS business question: ").strip()
            
            if query.lower() in ['quit', 'exit', 'q']:
                print("👋 Thanks for using SaaS Validator!")
                break
            
            if not query:
                print("Please enter a valid question.")
                continue
            
            print("\n🤔 Analyzing your query with Google Trends data...")
            result = await agent.run(query)
            
            if result["success"]:
                print("\n✅ Analysis completed!")
                
                if result.get("trends_data"):
                    print(f"📈 Retrieved Google Trends data for {len(result['trends_data'])} queries")
                
                print("\n💡 Recommendations:")
                for i, rec in enumerate(result["recommendations"], 1):
                    print(f"{i}. {rec}")
            else:
                print(f"\n❌ Error: {result.get('error', 'Unknown error')}")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")

async def main():
    """Main demo function"""
    print("Choose demo mode:")
    print("1. Automated demo with predefined queries")
    print("2. Interactive demo (ask your own questions)")
    print()
    
    choice = input("Enter your choice (1 or 2): ").strip()
    
    if choice == "2":
        await interactive_demo()
    else:
        await demo_agent()

if __name__ == "__main__":
    asyncio.run(main()) 