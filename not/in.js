import fs from 'fs';
import path from 'path';
import puppeteer from 'puppeteer';
import { fileURLToPath } from 'url';

// __dirname shim for ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

(async () => {
  // Paths
  const inputPath = path.join(__dirname, 'output', 'all.json');
  const outputDir = path.join(__dirname, 'in');
  const outputPath = path.join(outputDir, 'output2.json');

  // Load input data
  const raw = fs.readFileSync(inputPath, 'utf-8');
  const items = JSON.parse(raw);

  console.log(`Found ${items.length} entries. Starting scrape...`);

  // Puppeteer
  const browser = await puppeteer.launch({ headless: false });
  const page = await browser.newPage();

  for (let i = 0; i < items.length; i++) {
    const item = items[i];
    console.log(`(${i + 1}/${items.length}) Scraping: ${item.incubee}`);

    try {
      await page.goto(item.incubee, { waitUntil: 'domcontentloaded' });
      // Wait for the counts to appear
      await page.waitForSelector('.incubator-btn-wrapper .counts', { timeout: 3000 });

      // Extract counts
      const { current, graduated } = await page.evaluate(() => {
        const left = document.querySelector('.incubator-left-btn .counts')?.textContent.trim() || '';
        const right = document.querySelector('.incubator-right-btn .counts')?.textContent.trim() || '';
        return {
          current: parseInt(left.replace(/\D/g, ''), 10) || 0,
          graduated: parseInt(right.replace(/\D/g, ''), 10) || 0
        };
      });

      item.current_incubatees = current;
      item.graduated_incubatees = graduated;
    } catch (err) {
      console.error(`  Error scraping ${item.incubee}:`, err.message);
      item.current_incubatees = null;
      item.graduated_incubatees = null;
    }
  }

  await browser.close();

  // Ensure output directory exists
  fs.mkdirSync(outputDir, { recursive: true });
  // Write enriched data
  fs.writeFileSync(outputPath, JSON.stringify(items, null, 2), 'utf-8');

  console.log(`\n✅ Done! Results saved to ${outputPath}`);
  process.exit(0);
})();
