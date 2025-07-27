// NestJS Service Example for SaaS Validator Agent Integration
// This shows how to integrate the Python agent API with your NestJS backend

import { Injectable, HttpException, HttpStatus } from '@nestjs/common';
import { HttpService } from '@nestjs/axios';
import { firstValueFrom } from 'rxjs';

// Types for the API
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
  analysis_type?: string;
  processing_time?: number;
}

export interface BatchValidationRequest {
  queries: string[];
  include_trends?: boolean;
}

export interface BatchValidationResponse {
  success: boolean;
  results: ValidationResponse[];
  total_queries: number;
  successful_queries: number;
  failed_queries: number;
}

export interface HealthResponse {
  status: string;
  agent_ready: boolean;
  google_trends_available: boolean;
  timestamp: string;
}

@Injectable()
export class SaasValidatorService {
  private readonly apiBaseUrl: string;

  constructor(private readonly httpService: HttpService) {
    // Configure the Python agent API URL
    this.apiBaseUrl = process.env.SAAS_VALIDATOR_API_URL || 'http://localhost:8001';
  }

  /**
   * Validate a single SaaS business idea
   */
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

  /**
   * Validate multiple SaaS business ideas in batch
   */
  async validateSaaSBusinessIdeasBatch(request: BatchValidationRequest): Promise<BatchValidationResponse> {
    try {
      const response = await firstValueFrom(
        this.httpService.post<BatchValidationResponse>(
          `${this.apiBaseUrl}/validate/batch`,
          request
        )
      );

      return response.data;
    } catch (error) {
      throw new HttpException(
        `Failed to validate SaaS business ideas batch: ${error.message}`,
        HttpStatus.INTERNAL_SERVER_ERROR
      );
    }
  }

  /**
   * Get trending searches from Google Trends
   */
  async getTrendingSearches(country: string = 'US', limit: number = 10): Promise<any> {
    try {
      const response = await firstValueFrom(
        this.httpService.get(`${this.apiBaseUrl}/trends/trending`, {
          params: { country, limit }
        })
      );

      return response.data;
    } catch (error) {
      throw new HttpException(
        `Failed to get trending searches: ${error.message}`,
        HttpStatus.INTERNAL_SERVER_ERROR
      );
    }
  }

  /**
   * Get related queries for a keyword
   */
  async getRelatedQueries(keyword: string, country: string = 'US', limit: number = 10): Promise<any> {
    try {
      const response = await firstValueFrom(
        this.httpService.get(`${this.apiBaseUrl}/trends/related-queries`, {
          params: { keyword, country, limit }
        })
      );

      return response.data;
    } catch (error) {
      throw new HttpException(
        `Failed to get related queries: ${error.message}`,
        HttpStatus.INTERNAL_SERVER_ERROR
      );
    }
  }

  /**
   * Get interest over time for a keyword
   */
  async getInterestOverTime(keyword: string, country: string = 'US', timeframe: string = 'today 12-m'): Promise<any> {
    try {
      const response = await firstValueFrom(
        this.httpService.post(`${this.apiBaseUrl}/trends/interest-over-time`, {
          keyword,
          country,
          timeframe
        })
      );

      return response.data;
    } catch (error) {
      throw new HttpException(
        `Failed to get interest over time: ${error.message}`,
        HttpStatus.INTERNAL_SERVER_ERROR
      );
    }
  }

  /**
   * Check the health of the SaaS Validator agent
   */
  async checkHealth(): Promise<HealthResponse> {
    try {
      const response = await firstValueFrom(
        this.httpService.get<HealthResponse>(`${this.apiBaseUrl}/health`)
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

// NestJS Controller Example
import { Controller, Post, Get, Body, Query, Param } from '@nestjs/common';

@Controller('saas-validator')
export class SaasValidatorController {
  constructor(private readonly saasValidatorService: SaasValidatorService) { }

  @Post('validate')
  async validateSaaSBusinessIdea(@Body() request: ValidationRequest): Promise<ValidationResponse> {
    return this.saasValidatorService.validateSaaSBusinessIdea(request);
  }

  @Post('validate/batch')
  async validateSaaSBusinessIdeasBatch(@Body() request: BatchValidationRequest): Promise<BatchValidationResponse> {
    return this.saasValidatorService.validateSaaSBusinessIdeasBatch(request);
  }

  @Get('trends/trending')
  async getTrendingSearches(
    @Query('country') country: string = 'US',
    @Query('limit') limit: number = 10
  ): Promise<any> {
    return this.saasValidatorService.getTrendingSearches(country, limit);
  }

  @Get('trends/related-queries')
  async getRelatedQueries(
    @Query('keyword') keyword: string,
    @Query('country') country: string = 'US',
    @Query('limit') limit: number = 10
  ): Promise<any> {
    return this.saasValidatorService.getRelatedQueries(keyword, country, limit);
  }

  @Post('trends/interest-over-time')
  async getInterestOverTime(
    @Body() body: { keyword: string; country?: string; timeframe?: string }
  ): Promise<any> {
    return this.saasValidatorService.getInterestOverTime(
      body.keyword,
      body.country || 'US',
      body.timeframe || 'today 12-m'
    );
  }

  @Get('health')
  async checkHealth(): Promise<HealthResponse> {
    return this.saasValidatorService.checkHealth();
  }
}

// NestJS Module Example
import { Module } from '@nestjs/common';
import { HttpModule } from '@nestjs/axios';

@Module({
  imports: [HttpModule],
  controllers: [SaasValidatorController],
  providers: [SaasValidatorService],
  exports: [SaasValidatorService],
})
export class SaasValidatorModule { } 