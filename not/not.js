import axios from 'axios';
import fs from 'fs';
import path from 'path';

const fetchAllData = async () => {
  const url = 'https://api.meity.gov.in/search';  // API URL
  const headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Origin': 'https://msh.meity.gov.in',
    'Referer': 'https://msh.meity.gov.in/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
  };

  let allResults = [];
  let currentPage = 0;
  const pageSize = 70;  // Number of results per page
  const totalResults = 505;  // As per the total count you've shared

  // Loop to fetch all results until all pages are retrieved
  while (currentPage * pageSize < totalResults) {
    const data = {
      page: currentPage.toString(),
      page_size: pageSize,
      search_entity: "INCUBATOR",
    };

    try {
      const { data: responseData } = await axios.post(url, data, { headers });
      const results = responseData.results;

      if (results && results.length > 0) {
        allResults = [...allResults, ...results]; // Append new results to the allResults array
        console.log(`Page ${currentPage + 1} fetched, ${results.length} results added.`);
      } else {
        console.log(`No results found on page ${currentPage + 1}.`);
        break; // Exit if no results are found (edge case handling)
      }

      // Increment the page for the next request
      currentPage++;
    } catch (error) {
      console.error('Error fetching data from API:', error.message);
      break; // Exit on error
    }
  }

  console.log(`Total results fetched: ${allResults.length}`);

  // Save results to the out folder in all.json
  const outFolder = path.resolve('out');
  if (!fs.existsSync(outFolder)) {
    fs.mkdirSync(outFolder);  // Create the out folder if it doesn't exist
  }

  const filePath = path.join(outFolder, 'all.json');
  fs.writeFileSync(filePath, JSON.stringify(allResults, null, 2)); // Write to file with pretty formatting
  console.log(`Results saved to ${filePath}`);

  return allResults;
};

// Fetch all data
fetchAllData().then(allResults => {
  console.log('All results:', allResults);  // Process or save the results here
});
