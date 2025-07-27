#!/usr/bin/env python3
"""
SaaS Validator Agent Runner

This script provides a simple interface to run the SaaS Validator agent
and interact with it through the command line.
"""

import asyncio
import sys
import logging
from saas_validator_agent import SaaSValidatorAgent
from config import Config

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

async def interactive_mode():
    """Run the agent in interactive mode"""
    print("🚀 SaaS Validator Agent")
    print("=" * 50)
    print("This agent helps validate SaaS business ideas using Google Trends data.")
    print("Type 'quit' to exit.")
    print()
    
    # Validate configuration
    try:
        Config.validate()
        print("✅ Configuration validated")
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        return
    
    if not Config.MCP_SERVER_ENDPOINT:
        print("⚠️  Warning: MCP server endpoint not configured.")
        print("   The agent will work without Google Trends data.")
        print("   Set MCP_SERVER_ENDPOINT in config.py to enable trends analysis.")
        print()
    
    agent = SaaSValidatorAgent()
    
    while True:
        try:
            # Get user input
            user_query = input("\n💬 Enter your SaaS business question: ").strip()
            
            if user_query.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            if not user_query:
                print("Please enter a valid question.")
                continue
            
            print("\n🤔 Analyzing your query...")
            
            # Run the agent
            logging.info(f"Invoking agent with query: {user_query}")
            result = await agent.run(user_query)
            logging.info(f"Agent result: {result}")
            
            # Display results
            print("\n📊 Results:")
            print("-" * 30)
            
            if result["success"]:
                print("✅ Analysis completed successfully!")
                
                if result.get("trends_data"):
                    print(f"📈 Trends data retrieved for {len(result['trends_data'])} queries")
                
                print("\n💡 Recommendations:")
                for i, rec in enumerate(result["recommendations"], 1):
                    print(f"{i}. {rec}")
                    
            else:
                print(f"❌ Error: {result['error']}")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            logging.error(f"Error in agent invocation: {e}")
            print(f"❌ Unexpected error: {e}")

async def single_query_mode(query: str):
    """Run the agent for a single query"""
    print(f"🚀 SaaS Validator Agent - Single Query Mode")
    print(f"Query: {query}")
    print("=" * 50)
    
    try:
        Config.validate()
        agent = SaaSValidatorAgent()
        
        print("🤔 Analyzing your query...")
        logging.info(f"Invoking agent with query: {query}")
        result = await agent.run(query)
        logging.info(f"Agent result: {result}")
        
        if result["success"]:
            print("✅ Analysis completed successfully!")
            
            if result.get("trends_data"):
                print(f"📈 Trends data retrieved for {len(result['trends_data'])} queries")
            
            print("\n💡 Recommendations:")
            for i, rec in enumerate(result["recommendations"], 1):
                print(f"{i}. {rec}")
        else:
            print(f"❌ Error: {result['error']}")
            
    except Exception as e:
        logging.error(f"Error in agent invocation: {e}")
        print(f"❌ Error: {e}")

def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        # Single query mode
        query = " ".join(sys.argv[1:])
        asyncio.run(single_query_mode(query))
    else:
        # Interactive mode
        asyncio.run(interactive_mode())

if __name__ == "__main__":
    main() 