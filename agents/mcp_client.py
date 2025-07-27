#!/usr/bin/env python3
"""
Google Trends HTTP API Client

This module provides a client for the Google Trends HTTP API server.
Updated to work with the new mocked API endpoints.
"""

import asyncio
import json
import logging
from typing import Dict, Any, List, Optional
import httpx
from datetime import datetime, timedelta
from config import Config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GoogleTrendsAPI:
    """Google Trends HTTP API Client"""
    
    def __init__(self, base_url: str = None):
        """Initialize the Google Trends API client"""
        self.base_url = base_url or Config.GOOGLE_TRENDS_API_URL
        self.client = httpx.AsyncClient(timeout=30.0)
        logger.info(f"Initialized Google Trends API client for {self.base_url}")
    
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()
    
    async def health_check(self) -> bool:
        """Check if the Google Trends API is healthy"""
        try:
            response = await self.client.get(f"{self.base_url}/api/health")
            logger.info(f"Health check response: {response.status_code}")
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False
    
    async def get_trends_for_keywords(self, keywords: List[str]) -> Optional[Dict[str, Any]]:
        """Get trends data for multiple keywords using the new API format"""
        try:
            if not keywords:
                logger.warning("No keywords provided for trends analysis")
                return None
            
            # Join keywords with commas
            keywords_str = ",".join(keywords)
            logger.info(f"Fetching trends for keywords: {keywords_str}")
            
            # Call the new API endpoint
            response = await self.client.get(f"{self.base_url}/api/trends", params={"keywords": keywords_str})
            logger.info(f"Trends API response: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                #logger.info(f"Trends data received: {data}")
                return data
            else:
                logger.error(f"Failed to get trends: {response.status_code}")
                logger.error(f"Response content: {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error getting trends for keywords: {e}")
            return None
    
    async def get_trending_searches(self, country: str = "US", limit: int = 10) -> Optional[Dict[str, Any]]:
        """Get trending searches from Google Trends"""
        try:
            # Use the daily trends endpoint
            response = await self.client.get(f"{self.base_url}/api/trends/daily")
            logger.info(f"Daily trends response: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                # Limit the results
                trending_data = data.get("trending_searches", [])[:limit]
                return {
                    "trending_searches": trending_data,
                    "country": country,
                    "limit": limit
                }
            else:
                logger.error(f"Failed to get trending searches: {response.status_code}")
                return None
        except Exception as e:
            logger.error(f"Error getting trending searches: {e}")
            return None
    
    async def get_related_queries(self, keyword: str, country: str = "US", limit: int = 10) -> Optional[Dict[str, Any]]:
        """Get related queries for a keyword"""
        try:
            # Calculate date range (last 12 months)
            end_time = datetime.now()
            start_time = end_time - timedelta(days=365)
            
            params = {
                "keyword": keyword,
                "startTime": start_time.strftime("%Y-%m-%d"),
                "endTime": end_time.strftime("%Y-%m-%d")
            }
            
            logger.info(f"Calling related queries with params: {params}")
            response = await self.client.get(f"{self.base_url}/api/trends/related-queries", params=params)
            logger.info(f"Related queries response: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                # Limit the results
                related_queries = data.get("related_queries", [])[:limit]
                return {
                    "keyword": keyword,
                    "related_queries": related_queries,
                    "country": country,
                    "limit": limit
                }
            else:
                logger.error(f"Failed to get related queries: {response.status_code}")
                return None
        except Exception as e:
            logger.error(f"Error getting related queries: {e}")
            return None
    
    async def get_related_topics(self, keyword: str, country: str = "US", limit: int = 10) -> Optional[Dict[str, Any]]:
        """Get related topics for a keyword"""
        try:
            # Calculate date range (last 12 months)
            end_time = datetime.now()
            start_time = end_time - timedelta(days=365)
            
            params = {
                "keyword": keyword,
                "startTime": start_time.strftime("%Y-%m-%d"),
                "endTime": end_time.strftime("%Y-%m-%d")
            }
            
            logger.info(f"Calling related topics with params: {params}")
            response = await self.client.get(f"{self.base_url}/api/trends/related-topics", params=params)
            logger.info(f"Related topics response: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                # Limit the results
                related_topics = data.get("related_topics", [])[:limit]
                return {
                    "keyword": keyword,
                    "related_topics": related_topics,
                    "country": country,
                    "limit": limit
                }
            else:
                logger.error(f"Failed to get related topics: {response.status_code}")
                return None
        except Exception as e:
            logger.error(f"Error getting related topics: {e}")
            return None
    
    async def get_interest_over_time(self, keyword: str, country: str = "US", timeframe: str = "today 12-m") -> Optional[Dict[str, Any]]:
        """Get interest over time for a keyword"""
        try:
            # Calculate date range based on timeframe
            end_time = datetime.now()
            if "12-m" in timeframe:
                start_time = end_time - timedelta(days=365)
            elif "3-m" in timeframe:
                start_time = end_time - timedelta(days=90)
            elif "1-m" in timeframe:
                start_time = end_time - timedelta(days=30)
            else:
                start_time = end_time - timedelta(days=365)
            
            params = {
                "keyword": keyword,
                "startTime": start_time.strftime("%Y-%m-%d"),
                "endTime": end_time.strftime("%Y-%m-%d")
            }
            
            logger.info(f"Calling interest over time with params: {params}")
            response = await self.client.get(f"{self.base_url}/api/trends/interest-over-time", params=params)
            logger.info(f"Interest over time response: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"Interest over time data: {data}")
                return {
                    "keyword": keyword,
                    "interest_over_time": data.get("interest_over_time", {}),
                    "country": country,
                    "timeframe": timeframe
                }
            else:
                logger.error(f"Failed to get interest over time: {response.status_code}")
                logger.error(f"Response content: {response.text}")
                return None
        except Exception as e:
            logger.error(f"Error getting interest over time: {e}")
            return None
    
    async def get_interest_by_region(self, keyword: str, country: str = "US") -> Optional[Dict[str, Any]]:
        """Get interest by region for a keyword"""
        try:
            # Calculate date range (last 12 months)
            end_time = datetime.now()
            start_time = end_time - timedelta(days=365)
            
            params = {
                "keyword": keyword,
                "startTime": start_time.strftime("%Y-%m-%d"),
                "endTime": end_time.strftime("%Y-%m-%d")
            }
            
            logger.info(f"Calling interest by region with params: {params}")
            response = await self.client.get(f"{self.base_url}/api/trends/interest-by-region", params=params)
            logger.info(f"Interest by region response: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "keyword": keyword,
                    "interest_by_region": data.get("interest_by_region", {}),
                    "country": country
                }
            else:
                logger.error(f"Failed to get interest by region: {response.status_code}")
                return None
        except Exception as e:
            logger.error(f"Error getting interest by region: {e}")
            return None
    
    async def get_realtime_trends(self) -> Optional[Dict[str, Any]]:
        """Get realtime trends"""
        try:
            response = await self.client.get(f"{self.base_url}/api/trends/realtime")
            logger.info(f"Realtime trends response: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                return {
                    "realtime_trends": data.get("realtime_trends", []),
                    "timestamp": datetime.now().isoformat()
                }
            else:
                logger.error(f"Failed to get realtime trends: {response.status_code}")
                return None
        except Exception as e:
            logger.error(f"Error getting realtime trends: {e}")
            return None

# Legacy MCP Client for backward compatibility
class MCPClient:
    """Legacy MCP Client for backward compatibility"""
    
    def __init__(self, endpoint: str = None):
        """Initialize the MCP client"""
        self.endpoint = endpoint or Config.MCP_SERVER_ENDPOINT
        self.websocket = None
        self.client_id = None
        self.request_id = 0
    
    async def connect(self):
        """Connect to the MCP server"""
        # This is kept for backward compatibility
        # The new implementation uses HTTP API directly
        pass
    
    async def disconnect(self):
        """Disconnect from the MCP server"""
        # This is kept for backward compatibility
        pass
    
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Call a tool on the MCP server"""
        # This is kept for backward compatibility
        # The new implementation uses HTTP API directly
        pass

# Export the main client
__all__ = ["GoogleTrendsAPI", "MCPClient"] 