import fs from 'fs';
import path from 'path';

// Path to your JSON input file
const jsonPath = path.join('output', 'all.json');

// Path to save the CSV output
const csvPath = path.join('output', 'acc.csv');

try {
  const rawData = fs.readFileSync(jsonPath, 'utf-8');
  const data = JSON.parse(rawData);

  // Header
  let csv = 'incubator,location\n';

  // Process each item
  data.forEach(item => {
    const incubator = item.incubator.replace(/,/g, '');
    const location = item.location.replace(/,/g, '');
    csv += `${incubator},${location}\n`;
  });

  // Write to CSV file
  fs.writeFileSync(csvPath, csv, 'utf-8');
  console.log(`✅ CSV written to ${csvPath}`);
} catch (err) {
  console.error('❌ Error:', err.message);
}
