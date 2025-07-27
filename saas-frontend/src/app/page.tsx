'use client';

import { useState } from 'react';
import Image from 'next/image';
import { useRouter } from 'next/navigation';
import { mockValidationResult } from '@/lib/mockData';

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

export default function Home() {
  const [idea, setIdea] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!idea.trim()) return;

    setIsLoading(true);
    setError(null);

    try {
      // Simulate API delay
      await new Promise(resolve => setTimeout(resolve, 2000));

      // Call the real API
      const response = await fetch('http://localhost:8001/validate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: idea }),
      });

      if (!response.ok) {
        throw new Error(`API request failed: ${response.status}`);
      }

      const data: ValidationResult = await response.json();

      // Store data in session storage and navigate to results page
      const dataString = JSON.stringify(data);
      console.log('Storing data in session storage:', dataString.substring(0, 100) + '...');
      sessionStorage.setItem('validationResult', dataString);

      // Verify data was stored
      const stored = sessionStorage.getItem('validationResult');
      console.log('Data stored successfully:', stored ? 'Yes' : 'No');

      router.push('/result');

    } catch (err) {
      setError('Failed to validate idea. Please try again.');
      console.error('API Error:', err);
      setIsLoading(false);
    }
  };

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
              Where great ideas come to life
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-4xl mx-auto px-6 py-12">
        <div className="text-center mb-12">
          <h2 className="text-4xl font-bold text-slate-900 dark:text-white mb-4">
            Validate Your Ideas
          </h2>
          <p className="text-lg text-slate-600 dark:text-slate-300 max-w-2xl mx-auto">
            Share your ideas with our AI-powered validation engine and get instant insights on
            market potential, implementation strategy, and growth opportunities.
          </p>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="bg-white dark:bg-slate-800 rounded-2xl shadow-xl border border-slate-200 dark:border-slate-700 overflow-hidden">
            <div className="p-8">
              <label htmlFor="idea" className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-4">
                Describe your idea
              </label>
              <textarea
                id="idea"
                value={idea}
                onChange={(e) => setIdea(e.target.value)}
                placeholder="Tell us about your idea... What problem does it solve? Who is your target audience? What makes it unique? Include as much detail as possible to get the best validation results."
                className="w-full h-64 resize-none border-0 focus:ring-0 text-slate-900 dark:text-white bg-transparent placeholder-slate-400 dark:placeholder-slate-500 text-base leading-relaxed p-6 rounded-xl bg-slate-50 dark:bg-slate-700/50 border border-slate-200 dark:border-slate-600 focus:border-orange-300 dark:focus:border-orange-500 transition-colors duration-200"
                disabled={isLoading}
              />
            </div>

            {/* Character count and submit button */}
            <div className="px-8 py-6 bg-slate-50 dark:bg-slate-700/50 border-t border-slate-200 dark:border-slate-700 flex items-center justify-between">
              <div className="text-sm text-slate-500 dark:text-slate-400">
                {idea.length} characters
              </div>
              <button
                type="submit"
                disabled={!idea.trim() || isLoading}
                className="px-8 py-3 bg-gradient-to-r from-orange-500 to-orange-600 hover:from-orange-600 hover:to-orange-700 disabled:opacity-50 disabled:cursor-not-allowed text-white font-medium rounded-xl transition-all duration-200 transform hover:scale-105 active:scale-95 flex items-center space-x-2 shadow-lg"
              >
                {isLoading ? (
                  <>
                    <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                    <span>Analyzing...</span>
                  </>
                ) : (
                  <>
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                    </svg>
                    <span>Validate Idea</span>
                  </>
                )}
              </button>
            </div>
          </div>
        </form>

        {/* Loading State */}
        {isLoading && (
          <div className="mt-8 bg-white dark:bg-slate-800 rounded-2xl shadow-xl border border-slate-200 dark:border-slate-700 p-8">
            <div className="text-center">
              <div className="w-16 h-16 border-4 border-orange-200 border-t-orange-600 rounded-full animate-spin mx-auto mb-4"></div>
              <h3 className="text-xl font-semibold text-slate-900 dark:text-white mb-2">
                Analyzing Your Idea
              </h3>
              <p className="text-slate-600 dark:text-slate-300">
                Our AI is evaluating market trends, competition, and potential opportunities...
              </p>
              <div className="mt-4 flex justify-center space-x-2">
                <div className="w-2 h-2 bg-orange-400 rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-orange-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                <div className="w-2 h-2 bg-orange-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
              </div>
            </div>
          </div>
        )}

        {/* Error State */}
        {error && (
          <div className="mt-8 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-700 rounded-xl p-6">
            <div className="flex items-center space-x-3">
              <svg className="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <p className="text-red-800 dark:text-red-200">{error}</p>
            </div>
          </div>
        )}

        {/* Features */}
        <div className="mt-16 grid md:grid-cols-3 gap-8">
          <div className="text-center">
            <div className="w-12 h-12 bg-orange-100 dark:bg-orange-900/30 rounded-xl flex items-center justify-center mx-auto mb-4">
              <svg className="w-6 h-6 text-orange-600 dark:text-orange-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h3 className="font-semibold text-slate-900 dark:text-white mb-2">AI-Powered Analysis</h3>
            <p className="text-slate-600 dark:text-slate-300 text-sm">
              Advanced AI evaluates your idea's market potential and viability
            </p>
          </div>

          <div className="text-center">
            <div className="w-12 h-12 bg-orange-100 dark:bg-orange-900/30 rounded-xl flex items-center justify-center mx-auto mb-4">
              <svg className="w-6 h-6 text-orange-600 dark:text-orange-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <h3 className="font-semibold text-slate-900 dark:text-white mb-2">Actionable Insights</h3>
            <p className="text-slate-600 dark:text-slate-300 text-sm">
              Get detailed recommendations and next steps for your idea
            </p>
          </div>

          <div className="text-center">
            <div className="w-12 h-12 bg-orange-100 dark:bg-orange-900/30 rounded-xl flex items-center justify-center mx-auto mb-4">
              <svg className="w-6 h-6 text-orange-600 dark:text-orange-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h3 className="font-semibold text-slate-900 dark:text-white mb-2">Instant Results</h3>
            <p className="text-slate-600 dark:text-slate-300 text-sm">
              Receive comprehensive validation in seconds, not hours
            </p>
          </div>
        </div>

        {/* Footer */}
        <div className="mt-16 text-center">
          <p className="text-sm text-slate-500 dark:text-slate-400">
            Powered by advanced AI • Built for entrepreneurs and innovators
          </p>
        </div>
      </main>
    </div>
  );
}
