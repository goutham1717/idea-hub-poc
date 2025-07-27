// Test script for Google Trends Mock Server
import fetch from 'node-fetch';

const BASE_URL = 'http://localhost:3010';

async function testEndpoints() {
  console.log('Testing Google Trends Mock Server endpoints...\n');

  const tests = [
    {
      name: 'Health Check',
      url: `${BASE_URL}/api/health`,
      method: 'GET'
    },
    {
      name: 'Trends - Single Keyword (AI)',
      url: `${BASE_URL}/api/trends?keywords=artificial%20intelligence`,
      method: 'GET'
    },
    {
      name: 'Trends - Multiple Keywords (Food)',
      url: `${BASE_URL}/api/trends?keywords=coffee,milk,bread,pasta,steak`,
      method: 'GET'
    },
    {
      name: 'Trends - Tech Keywords',
      url: `${BASE_URL}/api/trends?keywords=blockchain,cryptocurrency,bitcoin,ethereum`,
      method: 'GET'
    },
    {
      name: 'Trends - With Date Range',
      url: `${BASE_URL}/api/trends?keywords=machine%20learning,deep%20learning&date=today%203-m`,
      method: 'GET'
    }
  ];

  for (const test of tests) {
    try {
      console.log(`Testing: ${test.name}`);
      const response = await fetch(test.url, { method: test.method });

      if (response.ok) {
        const data = await response.json();
        console.log(`✅ ${test.name} - SUCCESS`);
        console.log(`   Status: ${response.status}`);

        if (data.search_metadata) {
          console.log(`   Search ID: ${data.search_metadata.id}`);
          console.log(`   Keywords: ${data.search_parameters?.q || 'N/A'}`);
          console.log(`   Timeline data points: ${data.interest_over_time?.timeline_data?.length || 0}`);
          console.log(`   Averages: ${data.interest_over_time?.averages?.length || 0} keywords`);
        } else {
          console.log(`   Data keys: ${Object.keys(data).join(', ')}`);
        }
      } else {
        console.log(`❌ ${test.name} - FAILED`);
        console.log(`   Status: ${response.status}`);
        const errorData = await response.json().catch(() => ({}));
        console.log(`   Error: ${errorData.error || response.statusText}`);
      }
    } catch (error) {
      console.log(`❌ ${test.name} - ERROR`);
      console.log(`   Error: ${error.message}`);
    }
    console.log('');
  }

  console.log('Test completed!');
}

// Run tests
testEndpoints().catch(console.error); 