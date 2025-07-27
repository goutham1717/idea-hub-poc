import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for the SaaS Validator Agent"""
    
    # Anthropic API Key
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    
    # Google Trends API URL - Updated to new endpoint
    GOOGLE_TRENDS_API_URL = os.getenv("GOOGLE_TRENDS_API_URL", "http://localhost:3010")
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        if not cls.ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY environment variable is required")
        
        if not cls.GOOGLE_TRENDS_API_URL:
            raise ValueError("GOOGLE_TRENDS_API_URL environment variable is required")
        
        print(f"✅ Configuration validated")
        print(f"✅ Anthropic API Key: {'*' * 10 + cls.ANTHROPIC_API_KEY[-4:] if cls.ANTHROPIC_API_KEY else 'Not set'}")
        print(f"✅ Google Trends API: {cls.GOOGLE_TRENDS_API_URL}") 