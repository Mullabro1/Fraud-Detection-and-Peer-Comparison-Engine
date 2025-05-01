import fs from 'fs';
import path from 'path';

const inputPath = path.join('in', 'output.json');
const outputPath = path.join('out2', 'acc.csv');

// Read JSON file
const data = JSON.parse(fs.readFileSync(inputPath, 'utf-8'));

// Helper to sanitize commas from text fields
const sanitize = (text) => {
  if (typeof text !== 'string') return text;
  return text.replace(/,/g, '');
};

// CSV Header
const headers = ['incubator', 'location', 'incubee', 'current_incubatees', 'graduated_incubatees'];
const csvRows = [headers.join(',')];

// Process each entry
data.forEach(entry => {
  const row = [
    sanitize(entry.incubator),
    sanitize(entry.location),
    sanitize(entry.incubee),
    entry.current_incubatees ?? 0,
    entry.graduated_incubatees ?? 0
  ];
  csvRows.push(row.join(','));
});

// Write to CSV
fs.writeFileSync(outputPath, csvRows.join('\n'), 'utf-8');

console.log(`✅ CSV with nulls as 0 saved at ${outputPath}`);
