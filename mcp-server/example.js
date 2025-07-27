// Example usage of the Google Trends Mock Server API
// Run this file to test the API endpoints

import fetch from 'node-fetch';

const BASE_URL = 'http://localhost:3010';

async function testAPI() {
  console.log('Testing Google Trends Mock Server API...\n');

  try {
    // Test health endpoint
    console.log('1. Testing health endpoint...');
    const healthResponse = await fetch(`${BASE_URL}/api/health`);
    const healthData = await healthResponse.json();
    console.log('Health check result:', healthData);
    console.log('');

    // Test trends with single keyword
    console.log('2. Testing trends with single keyword "artificial intelligence"...');
    const singleTrendsResponse = await fetch(
      `${BASE_URL}/api/trends?keywords=artificial%20intelligence`
    );
    const singleTrendsData = await singleTrendsResponse.json();
    console.log('Single keyword trends result:');
    console.log(`- Search ID: ${singleTrendsData.search_metadata.id}`);
    console.log(`- Keywords: ${singleTrendsData.search_parameters.q}`);
    console.log(`- Timeline data points: ${singleTrendsData.interest_over_time.timeline_data.length}`);
    console.log(`- Average interest: ${singleTrendsData.interest_over_time.averages[0].value}`);
    console.log('');

    // Test trends with multiple keywords
    console.log('3. Testing trends with multiple keywords "coffee,milk,bread,pasta,steak"...');
    const multiTrendsResponse = await fetch(
      `${BASE_URL}/api/trends?keywords=coffee,milk,bread,pasta,steak`
    );
    const multiTrendsData = await multiTrendsResponse.json();
    console.log('Multiple keywords trends result:');
    console.log(`- Search ID: ${multiTrendsData.search_metadata.id}`);
    console.log(`- Keywords: ${multiTrendsData.search_parameters.q}`);
    console.log(`- Timeline data points: ${multiTrendsData.interest_over_time.timeline_data.length}`);
    console.log(`- Number of keywords: ${multiTrendsData.interest_over_time.averages.length}`);
    console.log('- Averages:');
    multiTrendsData.interest_over_time.averages.forEach(avg => {
      console.log(`  * ${avg.query}: ${avg.value}`);
    });
    console.log('');

    // Test trends with custom date range
    console.log('4. Testing trends with custom date range "today 3-m"...');
    const dateTrendsResponse = await fetch(
      `${BASE_URL}/api/trends?keywords=machine%20learning,deep%20learning&date=today%203-m`
    );
    const dateTrendsData = await dateTrendsResponse.json();
    console.log('Custom date range trends result:');
    console.log(`- Search ID: ${dateTrendsData.search_metadata.id}`);
    console.log(`- Keywords: ${dateTrendsData.search_parameters.q}`);
    console.log(`- Date range: ${dateTrendsData.search_parameters.date}`);
    console.log(`- Timeline data points: ${dateTrendsData.interest_over_time.timeline_data.length}`);
    console.log('');

    // Show sample timeline data
    console.log('5. Sample timeline data from the last response:');
    const sampleTimeline = dateTrendsData.interest_over_time.timeline_data.slice(0, 3);
    sampleTimeline.forEach((week, index) => {
      console.log(`Week ${index + 1}: ${week.date}`);
      week.values.forEach(value => {
        console.log(`  - ${value.query}: ${value.value}`);
      });
      console.log('');
    });

  } catch (error) {
    console.error('Error testing API:', error.message);
  }
}

// Run the test
testAPI(); 