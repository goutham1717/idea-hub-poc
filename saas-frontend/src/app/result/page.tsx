'use client';

import { useSearchParams, useRouter } from 'next/navigation';
import { useEffect, useState, useRef } from 'react';
import Image from 'next/image';

interface ValidationResult {
  success: boolean;
  query: string;
  recommendations: string[];
  trends_data: {
    interest_over_time: {
      timeline_data: Array<{
        date: string;
        values: Array<{
          query: string;
          value: string;
          extracted_value: number;
        }>;
      }>;
      averages: Array<{
        query: string;
        value: number;
      }>;
    };
  };
  opportunity_score: number;
  risk_score: number;
  recommendation: string;
  processing_time: number;
}

export default function ResultPage() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const [result, setResult] = useState<ValidationResult | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const hasProcessed = useRef(false);

  useEffect(() => {
    if (hasProcessed.current) return; // Prevent multiple executions

    try {
      // Get data from session storage
      console.log('Checking session storage...');
      const resultData = sessionStorage.getItem('validationResult');
      console.log('Data found in session storage:', resultData ? 'Yes' : 'No');

      if (resultData) {
        console.log('Parsing data...');
        const parsedResult = JSON.parse(resultData);
        console.log('Data parsed successfully');
        setResult(parsedResult);
        hasProcessed.current = true;
      } else {
        console.log('No data found in session storage');
        setError('No result data found. Please start a new analysis.');
        hasProcessed.current = true;
      }
    } catch (err) {
      console.error('Data parsing error:', err);
      setError('Invalid result data format. Please start a new analysis.');
      hasProcessed.current = true;
    }
    setLoading(false);
  }, []);

  // Clear session storage after successful processing
  useEffect(() => {
    if (result && !hasProcessed.current) {
      sessionStorage.removeItem('validationResult');
      console.log('Data cleared from session storage');
      hasProcessed.current = true;
    }
  }, [result]);

  const getScoreColor = (score: number, type: 'opportunity' | 'risk') => {
    if (type === 'opportunity') {
      if (score >= 8) return 'text-green-600 bg-green-100 dark:bg-green-900/30';
      if (score >= 6) return 'text-yellow-600 bg-yellow-100 dark:bg-yellow-900/30';
      return 'text-red-600 bg-red-100 dark:bg-red-900/30';
    } else {
      if (score <= 3) return 'text-green-600 bg-green-100 dark:bg-green-900/30';
      if (score <= 6) return 'text-yellow-600 bg-yellow-100 dark:bg-yellow-900/30';
      return 'text-red-600 bg-red-100 dark:bg-red-900/30';
    }
  };

  const getRecommendationColor = (recommendation: string) => {
    switch (recommendation) {
      case 'BUILD':
        return 'text-green-600 bg-green-100 dark:bg-green-900/30 border-green-200 dark:border-green-700';
      case 'VALIDATE':
        return 'text-yellow-600 bg-yellow-100 dark:bg-yellow-900/30 border-yellow-200 dark:border-yellow-700';
      case 'PIVOT':
        return 'text-red-600 bg-red-100 dark:bg-red-900/30 border-red-200 dark:border-red-700';
      default:
        return 'text-slate-600 bg-slate-100 dark:bg-slate-900/30 border-slate-200 dark:border-slate-700';
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800 flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-orange-200 border-t-orange-600 rounded-full animate-spin mx-auto mb-4"></div>
          <h3 className="text-xl font-semibold text-slate-900 dark:text-white mb-2">
            Loading Results
          </h3>
          <p className="text-slate-600 dark:text-slate-300">
            Preparing your analysis...
          </p>
        </div>
      </div>
    );
  }

  if (error || !result) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800 flex items-center justify-center">
        <div className="bg-white dark:bg-slate-800 rounded-2xl shadow-xl border border-slate-200 dark:border-slate-700 p-8 max-w-md mx-4">
          <div className="text-center">
            <div className="w-16 h-16 bg-red-100 dark:bg-red-900/30 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg className="w-8 h-8 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h3 className="text-xl font-semibold text-slate-900 dark:text-white mb-2">
              Error Loading Results
            </h3>
            <p className="text-slate-600 dark:text-slate-300 mb-6">
              {error || 'Unable to load analysis results'}
            </p>
            <button
              onClick={() => router.push('/')}
              className="px-6 py-3 bg-orange-500 hover:bg-orange-600 text-white font-medium rounded-xl transition-colors"
            >
              Start New Analysis
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800">
      {/* Header */}
      <header className="border-b border-slate-200 dark:border-slate-700 bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm">
        <div className="max-w-4xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-gradient-to-r from-orange-500 to-orange-600 rounded-xl flex items-center justify-center shadow-lg">
                <Image
                  src="/idea-hub-logo.svg"
                  alt="Idea Hub Logo"
                  width={32}
                  height={32}
                  className="rounded-lg"
                />
              </div>
              <h1 className="text-xl font-bold text-slate-900 dark:text-white">
                Idea Hub
              </h1>
            </div>
            <div className="text-sm text-slate-500 dark:text-slate-400">
              Analysis Results
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-4xl mx-auto px-6 py-12">
        <div className="space-y-8">
          {/* Header with back button */}
          <div className="flex items-center justify-between">
            <button
              onClick={() => router.push('/')}
              className="flex items-center space-x-2 text-slate-600 dark:text-slate-300 hover:text-slate-900 dark:hover:text-white transition-colors"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
              </svg>
              <span>New Analysis</span>
            </button>
            <div className="text-sm text-slate-500 dark:text-slate-400">
              Analysis completed in {result.processing_time.toFixed(1)}s
            </div>
          </div>

          {/* Original Query */}
          <div className="bg-white dark:bg-slate-800 rounded-2xl shadow-xl border border-slate-200 dark:border-slate-700 p-8">
            <h2 className="text-2xl font-bold text-slate-900 dark:text-white mb-4">
              Your Idea
            </h2>
            <div className="bg-slate-50 dark:bg-slate-700/50 rounded-xl p-6">
              <p className="text-slate-700 dark:text-slate-300 text-lg leading-relaxed">
                {result.query}
              </p>
            </div>
          </div>

          {/* Quick Assessment */}
          <div className="bg-white dark:bg-slate-800 rounded-2xl shadow-xl border border-slate-200 dark:border-slate-700 p-8">
            <h2 className="text-2xl font-bold text-slate-900 dark:text-white mb-6">
              Quick Assessment
            </h2>

            <div className="grid md:grid-cols-3 gap-6">
              {/* Opportunity Score */}
              <div className="text-center">
                <div className={`w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-3 ${getScoreColor(result.opportunity_score, 'opportunity')}`}>
                  <span className="text-2xl font-bold">{result.opportunity_score}/10</span>
                </div>
                <h3 className="font-semibold text-slate-900 dark:text-white mb-1">Opportunity Score</h3>
                <p className="text-sm text-slate-600 dark:text-slate-300">
                  Market potential & growth opportunity
                </p>
              </div>

              {/* Risk Score */}
              <div className="text-center">
                <div className={`w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-3 ${getScoreColor(result.risk_score, 'risk')}`}>
                  <span className="text-2xl font-bold">{result.risk_score}/10</span>
                </div>
                <h3 className="font-semibold text-slate-900 dark:text-white mb-1">Risk Score</h3>
                <p className="text-sm text-slate-600 dark:text-slate-300">
                  Market risks & challenges
                </p>
              </div>

              {/* Recommendation */}
              <div className="text-center">
                <div className={`w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-3 border-2 ${getRecommendationColor(result.recommendation)}`}>
                  <span className="text-lg font-bold">{result.recommendation}</span>
                </div>
                <h3 className="font-semibold text-slate-900 dark:text-white mb-1">Recommendation</h3>
                <p className="text-sm text-slate-600 dark:text-slate-300">
                  Our AI's verdict
                </p>
              </div>
            </div>
          </div>

          {/* Market Trends Chart */}
          <div className="bg-white dark:bg-slate-800 rounded-2xl shadow-xl border border-slate-200 dark:border-slate-700 p-8">
            <h2 className="text-2xl font-bold text-slate-900 dark:text-white mb-6">
              Market Trends Analysis
            </h2>

            <div className="space-y-4">
              {result.trends_data.interest_over_time.averages.map((avg, index) => (
                <div key={index} className="flex items-center justify-between p-4 bg-slate-50 dark:bg-slate-700/50 rounded-xl">
                  <span className="font-medium text-slate-900 dark:text-white">{avg.query}</span>
                  <div className="flex items-center space-x-3">
                    <div className="w-32 bg-slate-200 dark:bg-slate-600 rounded-full h-2">
                      <div
                        className="bg-orange-500 h-2 rounded-full transition-all duration-500"
                        style={{ width: `${avg.value}%` }}
                      ></div>
                    </div>
                    <span className="text-sm font-semibold text-slate-600 dark:text-slate-300 w-8 text-right">
                      {avg.value}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Detailed Recommendations */}
          <div className="bg-white dark:bg-slate-800 rounded-2xl shadow-xl border border-slate-200 dark:border-slate-700 p-8">
            <h2 className="text-2xl font-bold text-slate-900 dark:text-white mb-6">
              Detailed Recommendations
            </h2>

            <div className="prose prose-slate dark:prose-invert max-w-none">
              {result.recommendations.map((recommendation, index) => (
                <div key={index} className="mb-6 last:mb-0">
                  <div className="bg-slate-50 dark:bg-slate-700/50 rounded-xl p-6">
                    <div className="whitespace-pre-wrap text-slate-700 dark:text-slate-300 leading-relaxed">
                      {recommendation}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Share Results */}
          <div className="bg-white dark:bg-slate-800 rounded-2xl shadow-xl border border-slate-200 dark:border-slate-700 p-8">
            <h2 className="text-2xl font-bold text-slate-900 dark:text-white mb-6">
              Share Your Results
            </h2>
            <div className="flex flex-wrap gap-4">
              <button
                onClick={() => window.print()}
                className="px-6 py-3 bg-slate-100 dark:bg-slate-700 hover:bg-slate-200 dark:hover:bg-slate-600 text-slate-700 dark:text-slate-300 font-medium rounded-xl transition-colors flex items-center space-x-2"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z" />
                </svg>
                <span>Print Results</span>
              </button>
              <button
                onClick={() => {
                  const url = window.location.href;
                  navigator.clipboard.writeText(url);
                  alert('Results URL copied to clipboard!');
                }}
                className="px-6 py-3 bg-orange-500 hover:bg-orange-600 text-white font-medium rounded-xl transition-colors flex items-center space-x-2"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.367 2.684 3 3 0 00-5.367-2.684z" />
                </svg>
                <span>Share Results</span>
              </button>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
} 