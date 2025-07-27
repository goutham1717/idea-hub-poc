# NestJS Integration Guide for SaaS Validator Agent

This guide shows how to integrate the SaaS Validator agent with your NestJS backend.

## 🚀 Quick Start

### 1. Start the Python Agent API

First, start the Python agent API server:

```bash
# Install dependencies
pip install -r requirements.txt

# Start the API server
python nestjs_integration.py
```

The API will be available at `http://localhost:8001`

### 2. Test the API

```bash
# Health check
curl http://localhost:8001/health

# Validate a SaaS idea
curl -X POST http://localhost:8001/validate \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Should I build a SaaS for AI-powered project management?",
    "include_trends": true
  }'
```

## 📋 API Endpoints

### Core Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Health check |
| `POST` | `/validate` | Validate single SaaS idea |
| `POST` | `/validate/batch` | Validate multiple SaaS ideas |
| `GET` | `/trends/trending` | Get trending searches |
| `GET` | `/trends/related-queries` | Get related queries |
| `POST` | `/trends/interest-over-time` | Get interest over time |

### Request/Response Examples

#### Validate Single SaaS Idea

**Request:**
```json
{
  "query": "Should I build a SaaS for AI-powered customer support?",
  "include_trends": true,
  "max_queries": 3
}
```

**Response:**
```json
{
  "success": true,
  "query": "Should I build a SaaS for AI-powered customer support?",
  "recommendations": [
    "SaaS Validator Recommendations:",
    "Based on the trends analysis, consider the following..."
  ],
  "trends_data": {
    "AI-powered customer support": {
      "interest_over_time": {...},
      "related_queries": {...},
      "related_topics": {...}
    }
  },
  "processing_time": 2.45
}
```

#### Batch Validation

**Request:**
```json
{
  "queries": [
    "Should I build a SaaS for AI-powered project management?",
    "What are the trends in remote work software?",
    "Is there market demand for a new CRM solution?"
  ],
  "include_trends": true
}
```

**Response:**
```json
{
  "success": true,
  "results": [...],
  "total_queries": 3,
  "successful_queries": 3,
  "failed_queries": 0
}
```

## 🔧 NestJS Integration

### 1. Install Dependencies

```bash
npm install @nestjs/axios axios rxjs
npm install --save-dev @types/node
```

### 2. Create the Service

Create `saas-validator.service.ts`:

```typescript
import { Injectable, HttpException, HttpStatus } from '@nestjs/common';
import { HttpService } from '@nestjs/axios';
import { firstValueFrom } from 'rxjs';

export interface ValidationRequest {
  query: string;
  include_trends?: boolean;
  max_queries?: number;
}

export interface ValidationResponse {
  success: boolean;
  query: string;
  recommendations: string[];
  trends_data?: any;
  error?: string;
  processing_time?: number;
}

@Injectable()
export class SaasValidatorService {
  private readonly apiBaseUrl: string;

  constructor(private readonly httpService: HttpService) {
    this.apiBaseUrl = process.env.SAAS_VALIDATOR_API_URL || 'http://localhost:8001';
  }

  async validateSaaSBusinessIdea(request: ValidationRequest): Promise<ValidationResponse> {
    try {
      const response = await firstValueFrom(
        this.httpService.post<ValidationResponse>(
          `${this.apiBaseUrl}/validate`,
          request
        )
      );

      return response.data;
    } catch (error) {
      throw new HttpException(
        `Failed to validate SaaS business idea: ${error.message}`,
        HttpStatus.INTERNAL_SERVER_ERROR
      );
    }
  }

  async checkHealth(): Promise<any> {
    try {
      const response = await firstValueFrom(
        this.httpService.get(`${this.apiBaseUrl}/health`)
      );

      return response.data;
    } catch (error) {
      throw new HttpException(
        `Failed to check agent health: ${error.message}`,
        HttpStatus.INTERNAL_SERVER_ERROR
      );
    }
  }
}
```

### 3. Create the Controller

Create `saas-validator.controller.ts`:

```typescript
import { Controller, Post, Get, Body } from '@nestjs/common';
import { SaasValidatorService, ValidationRequest, ValidationResponse } from './saas-validator.service';

@Controller('saas-validator')
export class SaasValidatorController {
  constructor(private readonly saasValidatorService: SaasValidatorService) {}

  @Post('validate')
  async validateSaaSBusinessIdea(@Body() request: ValidationRequest): Promise<ValidationResponse> {
    return this.saasValidatorService.validateSaaSBusinessIdea(request);
  }

  @Get('health')
  async checkHealth(): Promise<any> {
    return this.saasValidatorService.checkHealth();
  }
}
```

### 4. Create the Module

Create `saas-validator.module.ts`:

```typescript
import { Module } from '@nestjs/common';
import { HttpModule } from '@nestjs/axios';
import { SaasValidatorController } from './saas-validator.controller';
import { SaasValidatorService } from './saas-validator.service';

@Module({
  imports: [HttpModule],
  controllers: [SaasValidatorController],
  providers: [SaasValidatorService],
  exports: [SaasValidatorService],
})
export class SaasValidatorModule {}
```

### 5. Import in Your App Module

```typescript
import { Module } from '@nestjs/common';
import { SaasValidatorModule } from './saas-validator/saas-validator.module';

@Module({
  imports: [SaasValidatorModule],
})
export class AppModule {}
```

## 🚀 Usage Examples

### Basic Usage

```typescript
// In your NestJS service
@Injectable()
export class BusinessIdeaService {
  constructor(private readonly saasValidatorService: SaasValidatorService) {}

  async validateBusinessIdea(idea: string) {
    const result = await this.saasValidatorService.validateSaaSBusinessIdea({
      query: idea,
      include_trends: true
    });

    return result;
  }
}
```

### Frontend Integration

```typescript
// In your frontend service
async validateSaaSIdea(query: string) {
  const response = await fetch('/api/saas-validator/validate', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      query,
      include_trends: true
    })
  });

  return response.json();
}
```

## 🔧 Configuration

### Environment Variables

```bash
# NestJS environment
SAAS_VALIDATOR_API_URL=http://localhost:8001

# Python agent environment
GOOGLE_TRENDS_API_URL=http://localhost:8000
ANTHROPIC_API_KEY=your-anthropic-key
```

### Docker Setup

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  saas-validator-api:
    build: .
    ports:
      - "8001:8001"
    environment:
      - GOOGLE_TRENDS_API_URL=http://google-trends-api:8000
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
    depends_on:
      - google-trends-api

  google-trends-api:
    # Your Google Trends API service
    image: your-google-trends-api
    ports:
      - "8000:8000"

  nestjs-app:
    build: ./nestjs-app
    ports:
      - "3000:3000"
    environment:
      - SAAS_VALIDATOR_API_URL=http://saas-validator-api:8001
    depends_on:
      - saas-validator-api
```

## 🧪 Testing

### Test the Python API

```bash
# Test health
curl http://localhost:8001/health

# Test validation
curl -X POST http://localhost:8001/validate \
  -H "Content-Type: application/json" \
  -d '{"query": "Should I build a SaaS for AI project management?"}'
```

### Test NestJS Integration

```bash
# Test NestJS endpoint
curl -X POST http://localhost:3000/saas-validator/validate \
  -H "Content-Type: application/json" \
  -d '{"query": "Should I build a SaaS for AI project management?"}'
```

## 🔍 Monitoring

### Health Checks

```typescript
// In your NestJS service
async checkAgentHealth() {
  const health = await this.saasValidatorService.checkHealth();
  
  if (!health.agent_ready) {
    // Handle agent not ready
  }
  
  if (!health.google_trends_available) {
    // Handle Google Trends not available
  }
  
  return health;
}
```

### Error Handling

```typescript
try {
  const result = await this.saasValidatorService.validateSaaSBusinessIdea(request);
  return result;
} catch (error) {
  if (error instanceof HttpException) {
    // Handle HTTP errors
    console.error('Validation failed:', error.message);
  } else {
    // Handle other errors
    console.error('Unexpected error:', error);
  }
  
  throw new HttpException(
    'SaaS validation service unavailable',
    HttpStatus.SERVICE_UNAVAILABLE
  );
}
```

## 🚀 Production Deployment

### 1. Environment Setup

```bash
# Production environment variables
export SAAS_VALIDATOR_API_URL=https://your-agent-api.com
export GOOGLE_TRENDS_API_URL=https://your-google-trends-api.com
export ANTHROPIC_API_KEY=your-production-key
```

### 2. Load Balancing

```nginx
# Nginx configuration
upstream saas_validator_api {
    server agent-api-1:8001;
    server agent-api-2:8001;
    server agent-api-3:8001;
}

server {
    listen 80;
    server_name your-domain.com;

    location /api/saas-validator/ {
        proxy_pass http://saas_validator_api;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 3. Monitoring

```typescript
// Add monitoring to your service
@Injectable()
export class SaasValidatorService {
  constructor(
    private readonly httpService: HttpService,
    private readonly metricsService: MetricsService
  ) {}

  async validateSaaSBusinessIdea(request: ValidationRequest): Promise<ValidationResponse> {
    const startTime = Date.now();
    
    try {
      const result = await this.callAgentAPI(request);
      
      // Record metrics
      this.metricsService.recordValidationSuccess(Date.now() - startTime);
      
      return result;
    } catch (error) {
      // Record error metrics
      this.metricsService.recordValidationError(error);
      throw error;
    }
  }
}
```

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [NestJS Documentation](https://docs.nestjs.com/)
- [HTTP Service Documentation](https://docs.nestjs.com/techniques/http-module)

## 🆘 Troubleshooting

### Common Issues

1. **Python API not starting**
   - Check if all dependencies are installed
   - Verify Google Trends API is running
   - Check logs for configuration errors

2. **NestJS can't connect to Python API**
   - Verify the API URL is correct
   - Check if CORS is properly configured
   - Ensure the Python API is running

3. **Google Trends data not available**
   - Check if Google Trends API server is running
   - Verify the API URL in configuration
   - Check network connectivity

### Debug Commands

```bash
# Check Python API health
curl http://localhost:8001/health

# Check Google Trends API health
curl http://localhost:8000/health

# Test NestJS endpoint
curl http://localhost:3000/saas-validator/health
``` 