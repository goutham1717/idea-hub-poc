import asyncio
import json
import time
from typing import Dict, Any, List, Optional
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_anthropic import ChatAnthropic
from langgraph.graph import StateGraph, END, START
from pydantic import BaseModel
from mcp_client import GoogleTrendsAPI, MCPClient
from config import Config
import logging

# Initialize configuration
Config.validate()

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

async def retry_with_backoff(func, max_retries=3, base_delay=1):
    """Retry function with exponential backoff for 529 errors"""
    for attempt in range(max_retries):
        try:
            return await func()
        except Exception as e:
            if "529" in str(e) or "overloaded" in str(e).lower():
                if attempt < max_retries - 1:
                    delay = base_delay * (2 ** attempt)  # Exponential backoff
                    print(f"Anthropic API overloaded (529 error). Retrying in {delay} seconds... (attempt {attempt + 1}/{max_retries})")
                    await asyncio.sleep(delay)
                    continue
                else:
                    print(f"Max retries reached. Returning fallback response.")
                    return None
            else:
                raise e
    return None

class AgentState(BaseModel):
    """State for the SaaS Validator agent"""
    messages: List[Any] = []
    user_query: str = ""
    analysis_result: Optional[Dict[str, Any]] = None
    trends_data: Optional[Dict[str, Any]] = None
    recommendations: List[str] = []
    error: Optional[str] = None

class SaaSValidatorAgent:
    def __init__(self):
        self.llm = ChatAnthropic(
            model="claude-3-5-sonnet-20241022",
            api_key=Config.ANTHROPIC_API_KEY,
            temperature=0.1
        )
        self.google_trends_api = GoogleTrendsAPI(Config.GOOGLE_TRENDS_API_URL)
        self.mcp_client = None  # Keep for legacy support
    
    async def run(self, user_query: str) -> Dict[str, Any]:
        """Run the SaaS Validator agent"""
        try:
            # Step 1: Analyze the query
            analysis_result = await self._analyze_query(user_query)
            
            # Step 2: Fetch trends if needed
            trends_data = None
            trends_analysis = None
            if analysis_result.get("needs_trends", False):
                trends_data = await self._fetch_trends(analysis_result.get("extracted_queries", [user_query]))
                if trends_data:
                    trends_analysis = await self._analyze_trends_and_score(trends_data)
            
            # Step 3: Generate recommendations
            recommendations = await self._generate_recommendations(user_query, trends_data)
            
            # Extract assessment scores
            opportunity_score = None
            risk_score = None
            recommendation = None
            
            if trends_analysis:
                opportunity_score = trends_analysis.get('opportunity_score')
                risk_score = trends_analysis.get('risk_score')
                recommendation = trends_analysis.get('recommendation')
            
            return {
                "success": True,
                "query": user_query,
                "recommendations": recommendations,
                "trends_data": trends_data,
                "opportunity_score": opportunity_score,
                "risk_score": risk_score,
                "recommendation": recommendation,
                "error": None
            }
            
        except Exception as e:
            return {
                "success": False,
                "query": user_query,
                "recommendations": [f"Error running agent: {str(e)}"],
                "opportunity_score": None,
                "risk_score": None,
                "recommendation": None,
                "error": str(e)
            }
        finally:
            if self.google_trends_api:
                await self.google_trends_api.close()
            if self.mcp_client:
                await self.mcp_client.disconnect()
    
    async def _analyze_query(self, user_query: str) -> Dict[str, Any]:
        """Analyze the user query to determine what type of analysis is needed"""
        try:
            logging.info(f"Calling _analyze_query with user_query: {user_query}")
            system_prompt = """You are a SaaS Validator agent that analyzes business ideas and market trends. 
            Analyze the user query and determine if it requires Google Trends data for validation.
            
            If the query is about:
            - Market research
            - Trend analysis
            - Business idea validation
            - Competitive analysis
            - Industry trends
            - SaaS business ideas
            - Product validation
            
            Then it likely needs Google Trends data.
            
            Respond with a JSON object containing:
            {
                "needs_trends": true/false,
                "extracted_queries": ["list", "of", "search", "terms"],
                "analysis_type": "market_research|trend_analysis|business_validation|competitive_analysis"
            }"""
            
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_query)
            ]
            
            response = await self.llm.ainvoke(messages)
            logging.info(f"_analyze_query response: {response}")
            
            # Parse the response to extract analysis info
            # For now, we'll assume it needs trends if it contains certain keywords
            needs_trends = any(keyword in user_query.lower() for keyword in 
                             ["trend", "market", "business", "idea", "validate", "research", "saas", "build", "should i", "can i"])
            
            # Extract relevant search terms from the query
            extracted_queries = []
            if "saas" in user_query.lower():
                # Extract the main topic from the query
                words = user_query.lower().split()
                for i, word in enumerate(words):
                    if word in ["saas", "app", "software", "platform", "tool"] and i + 1 < len(words):
                        # Get the next few words as the topic
                        topic = " ".join(words[i+1:i+4])
                        extracted_queries.append(topic)
            
            if not extracted_queries:
                # Fallback: extract key terms
                key_terms = ["ai", "project management", "crm", "remote work", "automation"]
                for term in key_terms:
                    if term in user_query.lower():
                        extracted_queries.append(term)
            
            if not extracted_queries:
                extracted_queries = [user_query]  # Use the full query as fallback
            
            return {
                "needs_trends": needs_trends,
                "extracted_queries": extracted_queries,
                "analysis_type": "market_research" if needs_trends else "general_analysis"
            }
            
        except Exception as e:
            logging.error(f"_analyze_query error: {e}")
            raise Exception(f"Error analyzing query: {str(e)}")
    
    async def _generate_keywords_from_query(self, user_query: str) -> List[str]:
        """Generate relevant keywords from the user query for trends analysis"""
        try:
            logging.info(f"Calling _generate_keywords_from_query with user_query: {user_query}")
            system_prompt = """You are a keyword generation expert for business trend analysis.
            
            Given a user query about a business idea or market opportunity, generate only 5 relevant keywords that would be useful for Google Trends analysis.
            
            For example:
            - Query: "Can I set up a cafe in Chennai?"
            - Keywords: ["coffee", "cafe", "restaurant", "food delivery", "Chennai", "coffee shop", "beverages", "dining"]
            
            - Query: "Should I build a SaaS for AI project management?"
            - Keywords: ["AI", "project management", "software", "automation", "machine learning", "productivity", "workflow", "collaboration"]
            
            Generate keywords that are:
            1. Relevant to the business idea
            2. Popular search terms
            3. Industry-specific
            4. Location-specific (if applicable)
            5. Product/service specific
            
            Return only the keywords as a comma-separated list, no explanations."""
            
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_query)
            ]
            
            async def invoke_llm():
                return await self.llm.ainvoke(messages)
            
            response = await retry_with_backoff(invoke_llm)
            logging.info(f"_generate_keywords_from_query response: {response}")
            
            if response is None:
                # Fallback: extract basic terms from query
                words = user_query.lower().split()
                basic_keywords = [word for word in words if len(word) > 3 and word not in ["should", "build", "create", "make", "start", "business", "idea"]]
                return basic_keywords[:5]
            
            # Parse the response to extract keywords
            keywords_text = response.content.strip()
            keywords = [kw.strip() for kw in keywords_text.split(",")]
            
            # Clean up keywords (remove quotes, extra spaces)
            cleaned_keywords = []
            for kw in keywords:
                kw = kw.strip().strip('"').strip("'")
                if kw and len(kw) > 1:  # Ensure keyword is not empty or too short
                    cleaned_keywords.append(kw)
            
            print(f"Generated keywords from query: {cleaned_keywords}")
            return cleaned_keywords[:10]  # Limit to 10 keywords
            
        except Exception as e:
            logging.error(f"_generate_keywords_from_query error: {e}")
            print(f"Error generating keywords: {e}")
            # Fallback: extract basic terms from query
            words = user_query.lower().split()
            basic_keywords = [word for word in words if len(word) > 3 and word not in ["should", "build", "create", "make", "start", "business", "idea"]]
            return basic_keywords[:5]
    
    async def _fetch_trends(self, queries: List[str]) -> Optional[Dict[str, Any]]:
        """Fetch Google Trends data using the new API format"""
        try:
            logging.info(f"Calling _fetch_trends with queries: {queries}")
            # Check if the API server is healthy
            #is_healthy = await self.google_trends_api.health_check()
            print("COMING HERE 1")
            is_healthy = True
            if not is_healthy:
                print("Warning: Google Trends API server is not healthy. Skipping trends data.")
                return None
            
            # Generate keywords from the first query (assuming it's the main user query)
            if queries:
                keywords = await self._generate_keywords_from_query(queries[0])
                print(f"Generated keywords for trends analysis: {keywords}")
                
                # Get trends data using the new API format
                trends_data = await self.google_trends_api.get_trends_for_keywords(keywords)
                #print(f"Trends data received: {trends_data}")
                logging.info(f"_fetch_trends response: {trends_data}")
                
                return trends_data
            
            return None
            
        except Exception as e:
            logging.error(f"_fetch_trends error: {e}")
            print(f"Warning: Error fetching trends: {str(e)}")
            return None
    
    async def _analyze_trends_and_score(self, trends_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze trends data and provide opportunity/risk scoring"""
        try:
            logging.info(f"Calling _analyze_trends_and_score with trends_data: {trends_data}")
            system_prompt = """You are a business analyst specializing in market opportunity assessment.
            
            Analyze the provided Google Trends data and provide:
            1. **Opportunity Score** (1-10): How good is the market opportunity?
            2. **Risk Score** (1-10): How risky is this business idea?
            3. **Trend Analysis**: What do the trends indicate?
            4. **Recommendation**: Should they build this business or not?
            5. **Key Insights**: What are the most important findings?
            
            Consider factors like:
            - Trend direction (rising/falling/stable)
            - Market size and growth
            - Competition level
            - Seasonal patterns
            - Geographic interest
            
            Respond with a JSON object:
            {
                "opportunity_score": 7,
                "risk_score": 4,
                "trend_analysis": "Trends show strong growth...",
                "recommendation": "BUILD" or "DON'T BUILD",
                "key_insights": ["insight1", "insight2"],
                "reasoning": "Detailed explanation..."
            }"""
            
            # Prepare context with trends data
            context = f"Google Trends Data:\n{json.dumps(trends_data, indent=2)}\n\nPlease analyze this data and provide scoring and recommendations."
            
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=context)
            ]
            
            async def invoke_llm():
                return await self.llm.ainvoke(messages)
            
            response = await retry_with_backoff(invoke_llm)
            logging.info(f"_analyze_trends_and_score response: {response}")
            
            if response is None:
                # Fallback response when API is overloaded
                return {
                    "opportunity_score": 5,
                    "risk_score": 5,
                    "trend_analysis": "Unable to analyze trends due to API overload. Please try again later.",
                    "recommendation": "ANALYZE FURTHER",
                    "key_insights": ["API temporarily unavailable"],
                    "reasoning": "The analysis service is currently overloaded. Please retry in a few minutes."
                }
            
            # Try to parse JSON response
            try:
                analysis = json.loads(response.content)
                return analysis
            except json.JSONDecodeError:
                # Fallback: return structured response
                return {
                    "opportunity_score": 5,
                    "risk_score": 5,
                    "trend_analysis": response.content,
                    "recommendation": "ANALYZE FURTHER",
                    "key_insights": ["Analysis completed"],
                    "reasoning": response.content
                }
            
        except Exception as e:
            logging.error(f"_analyze_trends_and_score error: {e}")
            print(f"Error analyzing trends: {e}")
            return {
                "opportunity_score": 5,
                "risk_score": 5,
                "trend_analysis": "Unable to analyze trends data",
                "recommendation": "ANALYZE FURTHER",
                "key_insights": ["Data analysis failed"],
                "reasoning": f"Error in analysis: {str(e)}"
            }
    
    async def _generate_recommendations(self, user_query: str, trends_data: Optional[Dict[str, Any]] = None) -> List[str]:
        """Generate final recommendations with trends analysis"""
        try:
            logging.info(f"Calling _generate_recommendations with user_query: {user_query}, trends_data: {trends_data}")
            system_prompt = """You are a SaaS Validator agent providing business recommendations. 
            Based on the user query and any available Google Trends data, provide actionable recommendations for:
            - Market validation
            - Business strategy
            - Risk assessment
            - Next steps
            
            Be specific, actionable, and business-focused. Use the trends data to support your recommendations."""
            
            # Prepare context for the LLM
            context = f"User Query: {user_query}\n"
            
            if trends_data:
                # Analyze trends and get scoring
                trends_analysis = await self._analyze_trends_and_score(trends_data)
                
                context += f"\n📊 TRENDS ANALYSIS:\n"
                context += f"Opportunity Score: {trends_analysis.get('opportunity_score', 'N/A')}/10\n"
                context += f"Risk Score: {trends_analysis.get('risk_score', 'N/A')}/10\n"
                context += f"Recommendation: {trends_analysis.get('recommendation', 'ANALYZE FURTHER')}\n"
                context += f"Trend Analysis: {trends_analysis.get('trend_analysis', 'N/A')}\n"
                context += f"Key Insights: {', '.join(trends_analysis.get('key_insights', []))}\n"
                context += f"Reasoning: {trends_analysis.get('reasoning', 'N/A')}\n"
                
                # Add raw trends data for context
                context += f"\nRaw Trends Data:\n{json.dumps(trends_data, indent=2)}\n"
            
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=context)
            ]
            
            async def invoke_llm():
                return await self.llm.ainvoke(messages)
            
            response = await retry_with_backoff(invoke_llm)
            logging.info(f"_generate_recommendations response: {response}")
            
            if response is None:
                # Fallback response when API is overloaded
                return [
                    "SaaS Validator Recommendations:",
                    "The analysis service is currently overloaded. Please try again in a few minutes.",
                    "In the meantime, here are some general recommendations:",
                    "1. Conduct market research to validate your business idea",
                    "2. Analyze your target market and competition",
                    "3. Create a minimum viable product (MVP)",
                    "4. Gather customer feedback early and often",
                    "5. Focus on solving a real problem for your customers"
                ]
            
            recommendations = [
                "SaaS Validator Recommendations:",
                response.content
            ]
            
            # Add trends analysis summary if available
            if trends_data:
                trends_analysis = await self._analyze_trends_and_score(trends_data)
                recommendations.append(f"\n🎯 QUICK ASSESSMENT:")
                recommendations.append(f"Opportunity Score: {trends_analysis.get('opportunity_score', 'N/A')}/10")
                recommendations.append(f"Risk Score: {trends_analysis.get('risk_score', 'N/A')}/10")
                recommendations.append(f"Recommendation: {trends_analysis.get('recommendation', 'ANALYZE FURTHER')}")
            
            return recommendations
            
        except Exception as e:
            logging.error(f"_generate_recommendations error: {e}")
            return [f"Error generating recommendations: {str(e)}"]

# Example usage
async def main():
    agent = SaaSValidatorAgent()
    
    # Example queries
    test_queries = [
        "Should I build a SaaS for AI-powered project management?",
        "What are the trends in remote work software?",
        "Is there market demand for a new CRM solution?"
    ]
    
    for query in test_queries:
        print(f"\n{'='*50}")
        print(f"Query: {query}")
        print(f"{'='*50}")
        
        result = await agent.run(query)
        
        if result["success"]:
            print("Recommendations:")
            for rec in result["recommendations"]:
                print(f"- {rec}")
        else:
            print(f"Error: {result['error']}")
        
        print()

if __name__ == "__main__":
    asyncio.run(main()) 