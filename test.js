import pkg from 'pg';  // Importing the pg package
import fs from 'fs';   // File system module to save JSON
import path from 'path';
import { fileURLToPath } from 'url';
import { execSync } from 'child_process';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);


const { Client } = pkg;

// PostgreSQL client configuration
const client = new Client({
  user: 'admin',
  host: 'localhost',
  database: 'excel',
  password: 'pass',
  port: 5433,
});

async function fetchDataAndSaveJSON() {
  try {
    await client.connect(); // Connect to PostgreSQL
    console.log('Starting execution of Python scripts...');

    const scripts = [
      'ml.py',
      'ml2.py',
      'ml3.py',
      'chat.py'
    ];

    const scriptsDir = path.join(__dirname, 'py');
    console.log(`Scripts will be executed from: ${scriptsDir}`);

    for (const script of scripts) {
      console.log(`Executing ${script}...`);
      const scriptPath = path.join(scriptsDir, script);
      execSync(`python "${scriptPath}"`, { stdio: 'inherit' });
    }
    

    // Query to get organization details
    const orgQuery = `SELECT * FROM organization;`;
    const orgResult = await client.query(orgQuery);

    let companies = [];

    for (const org of orgResult.rows) {
      const orgId = org.org_id;

      // Query to get all profit_loss records for the company
      const profitLossQuery = `
        SELECT data_range, type, profit_loss 
        FROM profit_loss 
        WHERE org_id = $1 
        ORDER BY data_range DESC;
      `;
      const profitLossResult = await client.query(profitLossQuery, [orgId]);

      // Query to get all balance_sheet records for the company
      const balanceSheetQuery = `
        SELECT data_range, type, networth 
        FROM balance_sheet 
        WHERE org_id = $1 
        ORDER BY data_range DESC;
      `;
      const balanceSheetResult = await client.query(balanceSheetQuery, [orgId]);

      // Combine financials into year-wise format
      let financials = {};

      // Process profit/loss data
      profitLossResult.rows.forEach(row => {
        if (!financials[row.data_range]) {
          financials[row.data_range] = {};
        }
        financials[row.data_range][row.type] = {
          ...financials[row.data_range][row.type],
          profit_loss: row.profit_loss
        };
      });

      // Process net worth data
      balanceSheetResult.rows.forEach(row => {
        if (!financials[row.data_range]) {
          financials[row.data_range] = {};
        }
        financials[row.data_range][row.type] = {
          ...financials[row.data_range][row.type],
          networth: row.networth
        };
      });

      // Construct JSON object
      companies.push({
        org_id: org.org_id,
        organization_name: org.name,
        cin: org.cin,
        org_type: org.type,
        status: org.status,
        corpository_sector: org.corpository_sector,
        pan: org.pan,
        lei: org.lei,
        amount_type: org.amount_type,
        email_id: org.email_id,
        website: org.website,
        telephone_number: org.telephone_number,
        financials: financials // Year-wise data
      });
    }

    // Ensure input folder exists
    const inputDir = path.join(process.cwd(), 'input');
    if (!fs.existsSync(inputDir)) {
      fs.mkdirSync(inputDir);
    }

    // Save JSON data to a file
    const filePath = path.join(inputDir, 'saved.json');
    fs.writeFileSync(filePath, JSON.stringify(companies, null, 2));

    console.log(`JSON file saved at: ${filePath}`);
  } catch (error) {
    console.error('Error fetching data:', error);
  } finally {
    await client.end(); // Close PostgreSQL connection
  }
}

fetchDataAndSaveJSON();
