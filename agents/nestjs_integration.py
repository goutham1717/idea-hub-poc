#!/usr/bin/env python3
"""
NestJS Integration for SaaS Validator Agent

This module provides a FastAPI wrapper that can be easily integrated
with NestJS backend using HTTP requests or gRPC.
Updated to work with the new Google Trends API at localhost:3010.
"""

import asyncio
import json
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from saas_validator_agent import SaaSValidatorAgent
from config import Config

# Initialize FastAPI app
app = FastAPI(
    title="SaaS Validator Agent API",
    description="API for SaaS business validation using Google Trends data",
    version="1.0.0"
)

# Add CORS middleware for NestJS integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the agent
agent = SaaSValidatorAgent()

# Pydantic models for request/response
class ValidationRequest(BaseModel):
    query: str = Field(..., description="SaaS business question to validate")
    include_trends: bool = Field(default=True, description="Whether to include Google Trends data")
    max_queries: int = Field(default=3, description="Maximum number of queries to analyze")

class ValidationResponse(BaseModel):
    success: bool
    query: str
    recommendations: List[str]
    trends_data: Optional[Dict[str, Any]] = None
    opportunity_score: Optional[int] = None
    risk_score: Optional[int] = None
    recommendation: Optional[str] = None
    error: Optional[str] = None
    analysis_type: Optional[str] = None
    processing_time: Optional[float] = None

class HealthResponse(BaseModel):
    status: str
    agent_ready: bool
    google_trends_available: bool
    timestamp: str

class BatchValidationRequest(BaseModel):
    queries: List[str] = Field(..., description="List of SaaS business questions to validate")
    include_trends: bool = Field(default=True, description="Whether to include Google Trends data")

class BatchValidationResponse(BaseModel):
    success: bool
    results: List[ValidationResponse]
    total_queries: int
    successful_queries: int
    failed_queries: int

@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint with API information"""
    return {
        "message": "SaaS Validator Agent API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    import datetime
    
    # Check if agent is ready
    agent_ready = True
    google_trends_available = False
    
    try:
        # Test Google Trends API
        is_healthy = await agent.google_trends_api.health_check()
        google_trends_available = is_healthy
    except Exception as e:
        print(f"Health check error: {e}")
    
    return HealthResponse(
        status="healthy",
        agent_ready=agent_ready,
        google_trends_available=google_trends_available,
        timestamp=datetime.datetime.now().isoformat()
    )

@app.post("/validate", response_model=ValidationResponse)
async def validate_saas_idea(request: ValidationRequest):
    """Validate a single SaaS business idea"""
    import time
    
    start_time = time.time()
    
    try:
        # Run the agent
        result = await agent.run(request.query)
        
        processing_time = time.time() - start_time
        
        return ValidationResponse(
            success=result["success"],
            query=result["query"],
            recommendations=result["recommendations"],
            trends_data=result.get("trends_data"),
            opportunity_score=result.get("opportunity_score"),
            risk_score=result.get("risk_score"),
            recommendation=result.get("recommendation"),
            error=result.get("error"),
            analysis_type=result.get("analysis_type"),
            processing_time=processing_time
        )
        
    except Exception as e:
        processing_time = time.time() - start_time
        return ValidationResponse(
            success=False,
            query=request.query,
            recommendations=[f"Error: {str(e)}"],
            opportunity_score=None,
            risk_score=None,
            recommendation=None,
            error=str(e),
            processing_time=processing_time
        )

@app.post("/validate/batch", response_model=BatchValidationResponse)
async def validate_saas_ideas_batch(request: BatchValidationRequest):
    """Validate multiple SaaS business ideas in batch"""
    import time
    
    start_time = time.time()
    results = []
    successful_count = 0
    failed_count = 0
    
    for query in request.queries:
        try:
            result = await agent.run(query)
            results.append(ValidationResponse(
                success=result["success"],
                query=result["query"],
                recommendations=result["recommendations"],
                trends_data=result.get("trends_data"),
                opportunity_score=result.get("opportunity_score"),
                risk_score=result.get("risk_score"),
                recommendation=result.get("recommendation"),
                error=result.get("error")
            ))
            
            if result["success"]:
                successful_count += 1
            else:
                failed_count += 1
                
        except Exception as e:
            results.append(ValidationResponse(
                success=False,
                query=query,
                recommendations=[f"Error: {str(e)}"],
                opportunity_score=None,
                risk_score=None,
                recommendation=None,
                error=str(e)
            ))
            failed_count += 1
    
    processing_time = time.time() - start_time
    
    return BatchValidationResponse(
        success=successful_count > 0,
        results=results,
        total_queries=len(request.queries),
        successful_queries=successful_count,
        failed_queries=failed_count
    )

@app.get("/trends/daily")
async def get_daily_trends():
    """Get daily trending searches from Google Trends"""
    try:
        result = await agent.google_trends_api.get_trending_searches()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching daily trends: {str(e)}")

@app.get("/trends/realtime")
async def get_realtime_trends():
    """Get realtime trends from Google Trends"""
    try:
        result = await agent.google_trends_api.get_realtime_trends()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching realtime trends: {str(e)}")

@app.get("/trends/related-queries")
async def get_related_queries(keyword: str, startTime: str = None, endTime: str = None):
    """Get related queries for a keyword"""
    try:
        result = await agent.google_trends_api.get_related_queries(keyword=keyword)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching related queries: {str(e)}")

@app.get("/trends/related-topics")
async def get_related_topics(keyword: str, startTime: str = None, endTime: str = None):
    """Get related topics for a keyword"""
    try:
        result = await agent.google_trends_api.get_related_topics(keyword=keyword)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching related topics: {str(e)}")

@app.get("/trends/interest-over-time")
async def get_interest_over_time(keyword: str, startTime: str = None, endTime: str = None):
    """Get interest over time for a keyword"""
    try:
        result = await agent.google_trends_api.get_interest_over_time(keyword=keyword)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching interest over time: {str(e)}")

@app.get("/trends/interest-by-region")
async def get_interest_by_region(keyword: str, startTime: str = None, endTime: str = None):
    """Get interest by region for a keyword"""
    try:
        result = await agent.google_trends_api.get_interest_by_region(keyword=keyword)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching interest by region: {str(e)}")

# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    """Initialize the agent on startup"""
    print("🚀 SaaS Validator Agent API starting...")
    try:
        Config.validate()
        print("✅ Configuration validated")
        print(f"✅ Google Trends API: {Config.GOOGLE_TRENDS_API_URL}")
    except Exception as e:
        print(f"❌ Configuration error: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    print("🛑 SaaS Validator Agent API shutting down...")
    try:
        await agent.google_trends_api.close()
        if agent.mcp_client:
            await agent.mcp_client.disconnect()
    except Exception as e:
        print(f"Warning: Error during shutdown: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001) 