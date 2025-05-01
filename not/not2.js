import fs from 'fs';
import path from 'path';

// Function to convert JSON to CSV
const convertJsonToCsv = (data) => {
  const header = ['name', 'city', 'state', 'country'];  // CSV Header
  const rows = data.map(item => [
    item.name || '',  // Name
    item.city || '',  // City
    item.state || '', // State
    item.country || '' // Country
  ]);

  // Convert the rows to CSV format
  const csvContent = [
    header.join(','),  // Join header fields
    ...rows.map(row => row.join(','))  // Join each row's fields
  ].join('\n');  // Join all lines

  return csvContent;
};

// Function to read all.json and convert it to CSV
const saveJsonAsCsv = async () => {
  try {
    // Load the all.json file (ensure the path is correct)
    const filePath = path.resolve('out', 'all.json');  // Assuming the file is in 'out' folder
    const jsonData = JSON.parse(fs.readFileSync(filePath, 'utf-8'));

    // Convert JSON to CSV
    const csvData = convertJsonToCsv(jsonData);

    // Save the CSV file in the same directory
    const csvFilePath = path.resolve('out', 'output.csv');
    fs.writeFileSync(csvFilePath, csvData);

    console.log('CSV file has been saved successfully!');
  } catch (error) {
    console.error('Error occurred:', error);
  }
};

// Execute the function
saveJsonAsCsv();
